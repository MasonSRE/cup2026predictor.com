#!/bin/zsh
# 定时更新开关（macOS launchd，每天 13:30 自动跑一次 update.sh）
#   ./schedule.sh on      开启
#   ./schedule.sh off     关闭
#   ./schedule.sh status  查看状态
set -e
LABEL="com.ai-worldcup-2026.update"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
DIR="$(cd "$(dirname "$0")" && pwd)"

case "${1:-status}" in
  on)
    mkdir -p "$HOME/Library/LaunchAgents" "$DIR/out"
    cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array><string>/bin/zsh</string><string>-lc</string>
    <string>cd $DIR &amp;&amp; ./update.sh >> out/update.log 2>&1</string></array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>13</integer><key>Minute</key><integer>30</integer></dict>
</dict></plist>
EOF
    launchctl unload "$PLIST" 2>/dev/null || true
    launchctl load "$PLIST"
    echo "已开启：每天 13:30 自动更新（日志 out/update.log）"
    ;;
  off)
    launchctl unload "$PLIST" 2>/dev/null || true
    rm -f "$PLIST"
    echo "已关闭定时更新"
    ;;
  status)
    if launchctl list 2>/dev/null | grep -q "$LABEL"; then
      echo "定时更新：已开启（每天 13:30）"
    else
      echo "定时更新：未开启。运行 ./schedule.sh on 开启"
    fi
    ;;
  *) echo "用法: ./schedule.sh on|off|status" ;;
esac
