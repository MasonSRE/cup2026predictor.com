"""比赛模型：Elo 胜率 → 泊松进球分布 → 比分抽样。

核心思路：
1. 用 Elo 等级分差计算 A 队的"胜负期望" We = 1 / (1 + 10^(-d/400))。
2. 把 We 映射成两队的期望进球数（实力越悬殊，总进球越多、份额越偏）。
3. 双泊松分布生成比分，叠加 Dixon-Coles 低比分修正（纯独立泊松会系统性
   低估 0-0/1-1 平局），淘汰赛打平则模拟加时（强度 1/3），再进点球大战。

所有比分分布按 (elo_a, elo_b) 缓存成累计分布，抽样时一次 bisect 完成，
使数万次全程模拟可以在几秒内跑完（纯标准库，零依赖）。
"""

from __future__ import annotations

import math
import random
from bisect import bisect_right
from functools import lru_cache

MAX_GOALS = 10          # 泊松分布截断到单队 10 球
HOST_ELO_BONUS = 60     # 东道主（墨/美/加）全程主场加成
BASE_TOTAL_GOALS = 2.6  # 势均力敌时的预期总进球（世界杯历史均值）
TOTAL_MISMATCH = 1.2    # 实力悬殊带来的总进球小幅上浮
GD_LINEAR = 2.4         # 胜负期望 → 期望净胜球的线性项
GD_CUBIC = 8.0          # 极端悬殊时净胜球的非线性增长项
MIN_LAMBDA = 0.08       # 单队期望进球下限
PENALTY_ELO_WEIGHT = 0.25  # 点球大战中 Elo 优势的衰减权重
DIXON_COLES_RHO = -0.10    # 低比分相关性修正（负值 → 抬高 0-0/1-1）
STYLE_MIN, STYLE_MAX = 0.80, 1.25  # 风格(开放度)对总进球的调节范围


def style_scale(team_a: dict, team_b: dict) -> float:
    """两队风格对总进球的乘数：开放度(att×def 相对值)的几何平均。

    胜负仍完全由 Elo 决定；风格只改变比分的"形状"——
    两支铁桶阵相遇偏 1-0/0-0，两支对攻队相遇 2-2/3-2 概率上浮。
    """
    s = (team_a.get("open", 1.0) * team_b.get("open", 1.0)) ** 0.5
    return round(min(max(s, STYLE_MIN), STYLE_MAX), 3)


def win_expectancy(elo_a: float, elo_b: float) -> float:
    """A 队的 Elo 胜负期望（0~1）。"""
    return 1.0 / (1.0 + 10 ** ((elo_b - elo_a) / 400.0))


def expected_goals(we: float) -> tuple[float, float]:
    """由胜负期望推出双方期望进球 (λa, λb)。

    思路：实力差决定"期望净胜球"而非进球份额——总进球围绕世界杯均值，
    净胜球随 Elo 差非线性增长，两队各取 (总±净胜)/2。
    这样弱队始终保有合理的进攻基线（不会出现 0.1 球的荒谬期望），
    比分分布里 2-1 / 3-1 / 2-2 等"双方都进球"的结果占比贴近真实。
    """
    x = we - 0.5
    total = BASE_TOTAL_GOALS + TOTAL_MISMATCH * abs(x)
    diff = GD_LINEAR * x + GD_CUBIC * x ** 3
    lam_a = max((total + diff) / 2.0, MIN_LAMBDA)
    lam_b = max((total - diff) / 2.0, MIN_LAMBDA)
    return lam_a, lam_b


def _poisson_pmf(lam: float, k: int) -> float:
    return math.exp(-lam) * lam ** k / math.factorial(k)


def score_distribution(elo_a: float, elo_b: float, tempo: float = 1.0,
                       style: float = 1.0, we_override: float | None = None):
    """(elo_a, elo_b) 对阵的比分累计分布。

    tempo < 1 用于加时赛（时间更短、进球更少）；style 为风格总进球乘数；
    we_override 用于市场赔率融合（直接给定胜负期望，跳过 Elo 推算）。
    返回 (cumulative_probs, scores)，scores[i] = (goals_a, goals_b)。
    """
    we = we_override if we_override is not None else win_expectancy(elo_a, elo_b)
    return _score_distribution_we(round(we, 4), tempo, style)


@lru_cache(maxsize=8192)
def _score_distribution_we(we: float, tempo: float = 1.0, style: float = 1.0):
    lam_a, lam_b = expected_goals(we)
    lam_a *= tempo * style
    lam_b *= tempo * style

    pmf_a = [_poisson_pmf(lam_a, k) for k in range(MAX_GOALS + 1)]
    pmf_b = [_poisson_pmf(lam_b, k) for k in range(MAX_GOALS + 1)]

    def dc_tau(ga: int, gb: int) -> float:
        """Dixon-Coles 修正系数，只作用于 0/1 比分区。"""
        rho = DIXON_COLES_RHO
        if ga == 0 and gb == 0:
            return 1 - lam_a * lam_b * rho
        if ga == 1 and gb == 0:
            return 1 + lam_b * rho
        if ga == 0 and gb == 1:
            return 1 + lam_a * rho
        if ga == 1 and gb == 1:
            return 1 - rho
        return 1.0

    scores: list[tuple[int, int]] = []
    cum: list[float] = []
    acc = 0.0
    for ga in range(MAX_GOALS + 1):
        for gb in range(MAX_GOALS + 1):
            acc += pmf_a[ga] * pmf_b[gb] * dc_tau(ga, gb)
            scores.append((ga, gb))
            cum.append(acc)
    # 截断后归一化
    cum = [c / acc for c in cum]
    return cum, scores


def effective_elo(team: dict) -> float:
    """东道主在本届比赛全程享受主场加成。"""
    return team["elo"] + (HOST_ELO_BONUS if team.get("host") else 0)


def sample_score(elo_a: float, elo_b: float, rng: random.Random,
                 tempo: float = 1.0, style: float = 1.0,
                 we_override: float | None = None) -> tuple[int, int]:
    cum, scores = score_distribution(elo_a, elo_b, tempo, style, we_override)
    return scores[bisect_right(cum, rng.random())]


def simulate_group_match(team_a: dict, team_b: dict, rng: random.Random,
                         we_override: float | None = None) -> tuple[int, int]:
    """小组赛：90 分钟比分，允许平局。"""
    return sample_score(effective_elo(team_a), effective_elo(team_b), rng,
                        style=style_scale(team_a, team_b),
                        we_override=we_override)


def simulate_knockout_match(team_a: dict, team_b: dict, rng: random.Random,
                            we_override: float | None = None) -> dict:
    """淘汰赛：必须分出胜负。返回 winner/loser 及过程信息。"""
    ea, eb = effective_elo(team_a), effective_elo(team_b)
    st = style_scale(team_a, team_b)
    ga, gb = sample_score(ea, eb, rng, style=st, we_override=we_override)
    via = "regular"
    if ga == gb:
        xa, xb = sample_score(ea, eb, rng, tempo=1 / 3, style=st,
                              we_override=we_override)
        ga, gb = ga + xa, gb + xb
        via = "extra_time"
        if ga == gb:
            via = "penalties"
            we = (we_override if we_override is not None
                  else win_expectancy(ea, eb))
            p_a = 0.5 + (we - 0.5) * PENALTY_ELO_WEIGHT
            if rng.random() < p_a:
                ga += 1
            else:
                gb += 1
    if ga > gb:
        winner, loser = team_a, team_b
    else:
        winner, loser = team_b, team_a
    return {"winner": winner, "loser": loser, "score": (ga, gb), "via": via}


def score_grid(team_a: dict, team_b: dict, size: int = 6,
               we_override: float | None = None) -> list[list[float]]:
    """比分概率矩阵：行 = A 队进球 0..size-1（末行/列聚合 size-1 球及以上）。"""
    ea, eb = effective_elo(team_a), effective_elo(team_b)
    cum, scores = score_distribution(ea, eb, style=style_scale(team_a, team_b),
                                     we_override=we_override)
    probs = [cum[0]] + [cum[i] - cum[i - 1] for i in range(1, len(cum))]
    grid = [[0.0] * size for _ in range(size)]
    for (ga, gb), p in zip(scores, probs):
        grid[min(ga, size - 1)][min(gb, size - 1)] += p
    return [[round(x, 4) for x in row] for row in grid]


def exact_score_prob(team_a: dict, team_b: dict, ga: int, gb: int,
                     we_override: float | None = None) -> float:
    """指定比分的精确概率。"""
    if ga > MAX_GOALS or gb > MAX_GOALS:
        return 0.0
    ea, eb = effective_elo(team_a), effective_elo(team_b)
    cum, _ = score_distribution(ea, eb, style=style_scale(team_a, team_b),
                                we_override=we_override)
    idx = ga * (MAX_GOALS + 1) + gb
    return cum[idx] - (cum[idx - 1] if idx else 0.0)


def match_probabilities(team_a: dict, team_b: dict, knockout: bool = False,
                        we_override: float | None = None) -> dict:
    """解析法计算单场胜平负概率与最可能比分（不做蒙特卡洛）。"""
    ea, eb = effective_elo(team_a), effective_elo(team_b)
    st = style_scale(team_a, team_b)
    we = we_override if we_override is not None else win_expectancy(ea, eb)
    cum, scores = score_distribution(ea, eb, style=st, we_override=we)
    probs = [cum[0]] + [cum[i] - cum[i - 1] for i in range(1, len(cum))]

    p_win = p_draw = p_loss = 0.0
    top_scores = sorted(zip(scores, probs), key=lambda x: -x[1])[:5]
    for (ga, gb), p in zip(scores, probs):
        if ga > gb:
            p_win += p
        elif ga == gb:
            p_draw += p
        else:
            p_loss += p

    # 比分首选与胜负判断保持一致：先定看好的结果，再在该结果内取最可能比分
    # （否则均势局会出现"看好主胜、比分却报 1-1"的矛盾——联合众数≠边际众数）
    outcome = ("H" if p_win >= max(p_draw, p_loss)
               else "D" if p_draw >= p_loss else "A")
    pick_score, pick_p = None, -1.0
    for (ga, gb), p in zip(scores, probs):
        ok = (ga > gb if outcome == "H"
              else ga == gb if outcome == "D" else ga < gb)
        if ok and p > pick_p:
            pick_score, pick_p = (ga, gb), p

    lam_a, lam_b = expected_goals(we)
    result = {
        "win_expectancy": we,
        "lambdas": (lam_a * st, lam_b * st),
        "p_win": p_win, "p_draw": p_draw, "p_loss": p_loss,
        "top_scores": top_scores,
        "outcome_pick": outcome,
        "outcome_score": (pick_score, pick_p),
    }
    if knockout:
        # 平局部分按加时/点球的近似胜率劈给双方
        et_edge = 0.5 + (we - 0.5) * 0.6  # 加时+点球综合优势（经验近似）
        result["p_advance_a"] = p_win + p_draw * et_edge
        result["p_advance_b"] = p_loss + p_draw * (1 - et_edge)
    return result
