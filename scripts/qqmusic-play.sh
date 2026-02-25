#!/bin/bash
# QQ音乐搜索播放脚本
# 用法: ./qqmusic-play.sh "歌手 歌名"
# 要求: cliclick 已安装

export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

QUERY="$1"
if [ -z "$QUERY" ]; then
    echo "用法: $0 \"歌手 歌名\""
    exit 1
fi

echo "🎵 搜索: $QUERY"

# 1. 激活 QQ Music
osascript -e 'tell application "QQMusic" to activate'
sleep 0.5
osascript -e '
tell application "System Events"
    tell process "QQMusic"
        set frontmost to true
    end tell
end tell'
sleep 0.3

# 2. 打开搜索框 (Edit > Search)
osascript -e '
tell application "System Events"
    tell process "QQMusic"
        click menu item "搜索" of menu "编辑" of menu bar 1
    end tell
end tell'
sleep 0.5

# 3. 清空搜索框
cliclick kd:cmd t:a ku:cmd
sleep 0.2
cliclick kp:delete
sleep 0.2

# 4. 用 osascript 设置剪贴板(避免编码乱码)，然后粘贴
osascript -e "set the clipboard to \"$QUERY\""
sleep 0.2
cliclick kd:cmd t:v ku:cmd
sleep 0.5

# 5. 按回车搜索
cliclick kp:return
sleep 2

# 6. 关闭下拉菜单
cliclick kp:esc
sleep 1

# 7. 双击第一首歌播放 (搜索结果列表第一行)
cliclick dc:385,463
sleep 1

echo "✅ 已播放: $QUERY"
