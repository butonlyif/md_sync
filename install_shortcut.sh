#!/bin/bash
# 创建 MDSync 快捷命令

# 添加到 zshrc
SHORTCUT='alias mdsync="open /Users/wangxin/Documents/trae_projects/md_sync/dist/MDSync.app"'
RC_FILE="$HOME/.zshrc"

# 检查是否已存在
if grep -q "alias mdsync" "$RC_FILE" 2>/dev/null; then
    echo "快捷命令已存在"
else
    echo "" >> "$RC_FILE"
    echo "# MDSync 快捷命令" >> "$RC_FILE"
    echo "$SHORTCUT" >> "$RC_FILE"
    echo "✓ 已添加快捷命令 'mdsync' 到 ~/.zshrc"
fi

# 创建桌面快捷方式
DESKTOP="$HOME/Desktop/MDSync.app"
if [ ! -e "$DESKTOP" ]; then
    ln -s "/Users/wangxin/Documents/trae_projects/md_sync/dist/MDSync.app" "$DESKTOP"
    echo "✓ 已在桌面创建快捷方式"
else
    echo "桌面快捷方式已存在"
fi

echo ""
echo "================================"
echo "安装完成！现在你可以："
echo ""
echo "1. 在终端输入: mdsync"
echo "2. 双击桌面上的 MDSync.app 图标"
echo "================================"
