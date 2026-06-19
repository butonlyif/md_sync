import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from config_manager import ConfigManager
from sync_engine import SyncEngine

class MDSyncApp:
    """MD 文件同步工具主界面"""

    def __init__(self, root):
        self.root = root
        self.root.title("MD 文件同步工具")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)

        self.config = ConfigManager()

        self.setup_ui()

    def setup_ui(self):
        """初始化界面"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Obsidian 路径设置区域
        path_frame = ttk.LabelFrame(main_frame, text="Obsidian 路径", padding="5")
        path_frame.pack(fill=tk.X, pady=(0, 10))

        self.path_var = tk.StringVar(value=self.config.get_obsidian_path())
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=60)
        path_entry.pack(side=tk.LEFT, padx=(5, 5))

        ttk.Button(path_frame, text="浏览...", command=self.browse_obsidian_path).pack(side=tk.LEFT)

        # 项目管理区域
        project_frame = ttk.LabelFrame(main_frame, text="项目列表", padding="5")
        project_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 创建树形视图显示项目
        tree_frame = ttk.Frame(project_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("name", "path", "subdir"), show="headings", height=10)
        self.tree.heading("name", text="项目名称")
        self.tree.heading("path", text="项目路径")
        self.tree.heading("subdir", text="Obsidian 子目录")
        self.tree.column("name", width=120)
        self.tree.column("path", width=300)
        self.tree.column("subdir", width=150)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 项目操作按钮
        btn_frame = ttk.Frame(project_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(btn_frame, text="添加项目", command=self.add_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除选中", command=self.delete_project).pack(side=tk.LEFT, padx=5)

        # 同步按钮
        sync_frame = ttk.Frame(main_frame)
        sync_frame.pack(fill=tk.X)

        self.sync_btn = ttk.Button(sync_frame, text="同步所有项目", command=self.sync_all_projects, style="Accent.TButton")
        self.sync_btn.pack(pady=10)

        # 状态显示区域
        status_frame = ttk.LabelFrame(main_frame, text="同步状态", padding="5")
        status_frame.pack(fill=tk.BOTH, expand=True)

        self.status_text = tk.Text(status_frame, height=8, wrap=tk.WORD, state=tk.DISABLED)
        self.status_text.pack(fill=tk.BOTH, expand=True)

        scrollbar_status = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar_status.set)
        scrollbar_status.pack(side=tk.RIGHT, fill=tk.Y)

        # 加载已有项目
        self.refresh_projects()

    def browse_obsidian_path(self):
        """浏览选择 Obsidian 路径"""
        path = filedialog.askdirectory(title="选择 Obsidian 笔记库路径")
        if path:
            self.path_var.set(path)
            self.config.set_obsidian_path(path)
            self.log(f"已设置 Obsidian 路径: {path}")

    def add_project(self):
        """添加新项目"""
        # 弹出对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("添加项目")
        dialog.geometry("500x280")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(True, True)  # 允许调整大小
        
        # 主容器
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 项目名称
        ttk.Label(main_frame, text="项目名称:").grid(row=0, column=0, sticky=tk.W, pady=3)
        name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=name_var, width=45).grid(row=1, column=0, sticky=tk.EW, pady=3)

        # 项目路径
        ttk.Label(main_frame, text="项目路径:").grid(row=2, column=0, sticky=tk.W, pady=3)
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=3, column=0, sticky=tk.EW, pady=3)
        path_var = tk.StringVar()
        ttk.Entry(path_frame, textvariable=path_var, width=40).pack(side=tk.LEFT)
        ttk.Button(path_frame, text="浏览...", command=lambda: self.select_project_path(path_var)).pack(side=tk.LEFT, padx=5)

        # Obsidian 子目录
        ttk.Label(main_frame, text="Obsidian 子目录:").grid(row=4, column=0, sticky=tk.W, pady=3)
        subdir_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=subdir_var, width=45).grid(row=5, column=0, sticky=tk.EW, pady=3)
        ttk.Label(main_frame, text="（留空则复制到 Obsidian 根目录）", font=('Arial', 8)).grid(row=6, column=0, sticky=tk.W, pady=(0, 5))

        # 按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=7, column=0, sticky=tk.EW, pady=10)

        def confirm():
            name = name_var.get().strip()
            path = path_var.get().strip()
            subdir = subdir_var.get().strip()
            if not name or not path:
                messagebox.showerror("错误", "请填写项目名称和路径")
                return

            if self.config.add_project(name, path, subdir):
                self.refresh_projects()
                self.log(f"已添加项目: {name} -> {subdir if subdir else '/'}")
                dialog.destroy()
                return
            else:
                messagebox.showerror("错误", f"项目 '{name}' 已存在")
                return

        ttk.Button(btn_frame, text="确定", command=confirm, width=15).pack(side=tk.RIGHT)

    def select_project_path(self, path_var):
        """选择项目路径"""
        path = filedialog.askdirectory(title="选择项目目录")
        if path:
            path_var.set(path)

    def delete_project(self):
        """删除选中的项目"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要删除的项目")
            return

        for item in selection:
            item_data = self.tree.item(item)
            name = item_data['values'][0]
            self.config.remove_project(name)
            self.log(f"已删除项目: {name}")

        self.refresh_projects()

    def refresh_projects(self):
        """刷新项目列表"""
        # 清空现有项目
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 添加项目
        for project in self.config.get_projects():
            subdir = project.get('subdir', '')
            self.tree.insert("", tk.END, values=(project['name'], project['path'], subdir))

    def log(self, message: str):
        """在状态区域打印日志"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)

    def sync_all_projects(self):
        """同步所有项目"""
        obsidian_path = self.config.get_obsidian_path()
        if not obsidian_path:
            messagebox.showerror("错误", "请先设置 Obsidian 路径")
            return

        projects = self.config.get_projects()
        if not projects:
            messagebox.showwarning("警告", "没有可同步的项目")
            return

        self.log("=" * 50)
        self.log("开始同步...")
        self.log("=" * 50)

        engine = SyncEngine(obsidian_path)
        results = engine.sync_all(projects)

        total_files = 0
        total_copied = 0
        total_updated = 0
        total_skipped = 0

        for result in results:
            subdir = result.get('subdir', '')
            self.log(f"\n项目: {result['name']} -> {subdir if subdir else '/'}")
            self.log(f"  总文件数: {result['total']}")
            self.log(f"  新增: {result['copied']}")
            self.log(f"  更新: {result['updated']}")
            self.log(f"  跳过: {result['skipped']}")

            if result['errors']:
                self.log(f"  错误:")
                for error in result['errors']:
                    self.log(f"    - {error}")

            total_files += result['total']
            total_copied += result['copied']
            total_updated += result['updated']
            total_skipped += result['skipped']

        self.log("\n" + "=" * 50)
        self.log(f"同步完成！共处理 {total_files} 个文件")
        self.log(f"新增: {total_copied}, 更新: {total_updated}, 跳过: {total_skipped}")
        self.log("=" * 50)

def main():
    import os
    os.environ['TK_SILENCE_DEPRECATION'] = '1'
    
    root = tk.Tk()

    # 设置样式 - 使用更兼容的配置
    try:
        style = ttk.Style()
        # 尝试使用 native 主题，失败则使用默认
        if 'aqua' in style.theme_names():
            style.theme_use('aqua')
        elif 'clam' in style.theme_names():
            style.theme_use('clam')
    except:
        pass

    app = MDSyncApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
