#!/usr/bin/env python3
import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
from tkinter import ttk

# macOS 需要这个
try:
    from matplotlib.backends._macosx import NavigationToolbar2CT
except:
    pass

root = tk.Tk()
root.title("测试窗口")
root.geometry("800x600")

# 设置窗口在屏幕中央
root.eval('tk::PlaceWindow . center')

# 测试普通 Frame
frame1 = tk.Frame(root, bg='lightblue', height=100)
frame1.pack(fill=tk.X, padx=10, pady=10)

label1 = tk.Label(frame1, text="这是一个测试标签", bg='lightblue', fg='black', font=("Arial", 16))
label1.pack(pady=20)

# 测试按钮
btn = ttk.Button(root, text="测试按钮")
btn.pack(pady=20)

# 确保窗口可见
root.deiconify()
root.lift()
root.focus_force()

root.mainloop()
