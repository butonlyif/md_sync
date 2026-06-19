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
