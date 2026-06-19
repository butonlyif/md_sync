#!/bin/bash
# MD 文件同步工具启动脚本
export TK_SILENCE_DEPRECATION=1
cd "$(dirname "$0")"
/usr/bin/python3 main.py
