#!/bin/bash
# 重新创建 macOS 应用包

APP_NAME="MDSync"
APP_DIR="/Users/wangxin/Documents/trae_projects/md_sync/${APP_NAME}.app/Contents/MacOS"

# 删除旧的应用
rm -rf "/Users/wangxin/Documents/trae_projects/md_sync/${APP_NAME}.app"

# 创建目录结构
mkdir -p "$APP_DIR"

# 复制所有 Python 文件
cp main.py ui.py config_manager.py sync_engine.py "$APP_DIR/"

# 创建启动脚本
cat > "$APP_DIR/main.py" << 'PYEOF'
#!/usr/bin/env python3.10
import os
import sys

os.environ['TK_SILENCE_DEPRECATION'] = '1'

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# MacOS -> Contents -> MDSync.app -> md_sync
# 向上两级到 Contents，然后上一级到 app 名称，然后上一级到项目目录
app_dir = os.path.dirname(script_dir)  # Contents
app_parent = os.path.dirname(app_dir)  # MDSync.app
project_dir = os.path.dirname(app_parent)  # md_sync

# 添加项目根目录到 Python 路径
sys.path.insert(0, project_dir)

# 切换到项目目录
os.chdir(project_dir)

from ui import main

if __name__ == "__main__":
    main()
PYEOF

chmod +x "$APP_DIR/main.py"

# 创建 Info.plist
cat > "/Users/wangxin/Documents/trae_projects/md_sync/${APP_NAME}.app/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>main.py</string>
    <key>CFBundleName</key>
    <string>MDSync</string>
    <key>CFBundleDisplayName</key>
    <string>MD 文件同步工具</string>
    <key>CFBundleIdentifier</key>
    <string>com.mdsync.app</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.9</string>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.utilities</string>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

echo "应用已重新创建: /Users/wangxin/Documents/trae_projects/md_sync/${APP_NAME}.app"
