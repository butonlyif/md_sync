# Markdown Sync Tool

## 项目描述
Markdown Sync Tool 是一个用于同步和备份 Markdown 文件的工具，支持 Obsidian 笔记和其他 Markdown 文档。

## 主要功能
- Markdown 文件同步
- Obsidian 笔记同步
- 文件备份
- 增量更新

## 技术栈
- Python
- Tkinter (GUI)
- 文件系统操作

## 项目结构
```
md_sync/
├── main.py                  # 主程序
├── sync_engine.py          # 同步引擎
├── ui.py                   # 用户界面
├── main_debug.py           # 调试版本
├── requirements.txt        # 依赖
├── dist/                   # 分发包
└── assets/                 # 资源文件
```

## 开发注意事项
- 支持文件过滤和排除规则
- 增量同步节省带宽
- GUI 使用 Tkinter
- 支持 macOS/Windows/Linux
