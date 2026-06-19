#!/usr/bin/env python3.10
"""
MD 文件同步工具 - 带错误日志
"""
import os
import sys
import traceback

# 错误日志文件
log_file = os.path.expanduser("~/Library/Logs/MDSync/error.log")
os.makedirs(os.path.dirname(log_file), exist_ok=True)

try:
    os.environ['TK_SILENCE_DEPRECATION'] = '1'
    
    # 重定向错误输出
    sys.stderr = open(log_file, 'a')
    print(f"启动应用 - {os.getpid()}", file=sys.stderr)
    sys.stderr.flush()
    
    from ui import main
    main()
    
except Exception as e:
    error_msg = f"""
========== MDSync Error ==========
时间: {os.popen('date').read().strip()}
错误: {str(e)}
==================================
{traceback.format_exc()}
"""
    print(error_msg, file=sys.stderr)
    sys.stderr.flush()
    
    # 显示错误对话框
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("MDSync 错误", f"应用启动失败:\n{str(e)}\n\n详细信息已保存到日志文件")
        root.destroy()
    except:
        pass
    
    sys.exit(1)
