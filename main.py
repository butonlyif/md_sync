#!/usr/bin/env python3.10
"""
MD 文件同步工具
将项目中的所有 md 文件同步到 Obsidian 笔记本库
"""
import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

from ui import main

if __name__ == "__main__":
    main()
