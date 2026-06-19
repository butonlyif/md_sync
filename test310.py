#!/usr/bin/env python3
import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Python 3.10 测试窗口")
root.geometry("800x600")

# 测试 Frame
frame = tk.Frame(root, bg='lightblue', height=100)
frame.pack(fill=tk.X, padx=10, pady=10)

label = tk.Label(frame, text="Python 3.10 测试成功！", bg='lightblue', fg='black', font=("Arial", 20))
label.pack(pady=20)

# 测试按钮
ttk.Button(root, text="测试按钮").pack(pady=20)

root.mainloop()
