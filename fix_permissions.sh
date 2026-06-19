#!/bin/bash
# 修复 MDSync 应用权限

APP_PATH="/Users/wangxin/Documents/trae_projects/md_sync/dist/MDSync.app"

echo "正在修复 MDSync 应用权限..."
echo ""

# 1. 移除扩展属性（quarantine）
echo "1. 移除安全限制标记..."
xattr -rd com.apple.quarantine "$APP_PATH" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✓ 已移除 quarantine 标记"
else
    echo "   ! 无法移除 quarantine 标记（可能需要手动操作）"
fi

# 2. 设置正确的权限
echo ""
echo "2. 设置应用权限..."
chmod -R 755 "$APP_PATH"
echo "   ✓ 权限已设置"

# 3. 签名应用（如果可以）
echo ""
echo "3. 尝试签名应用..."
codesign -f -s - "$APP_PATH/Contents/MacOS/MDSync" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✓ 应用已签名"
else
    echo "   ! 无法签名（需要 Apple 开发者账号）"
fi

echo ""
echo "================================"
echo "修复完成！请尝试以下方法之一："
echo ""
echo "方法 1：直接双击 MDSync.app"
echo "方法 2：右键点击 -> 选择\"打开\""
echo "方法 3：在终端运行: open $APP_PATH"
echo ""
echo "如果还是不行，请运行:"
echo "  sudo xattr -rd com.apple.quarantine $APP_PATH"
echo "================================"
