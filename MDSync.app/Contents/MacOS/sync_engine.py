import os
import shutil
from pathlib import Path
from typing import List, Dict

class SyncEngine:
    """同步引擎，负责查找和复制 md 文件"""

    def __init__(self, obsidian_path: str):
        self.obsidian_path = Path(obsidian_path)

    def find_md_files(self, project_path: str) -> List[Path]:
        """递归查找目录下所有 md 文件"""
        md_files = []
        project_path = Path(project_path)

        if not project_path.exists():
            return md_files

        for root, dirs, files in os.walk(project_path):
            # 跳过隐藏目录（如 .git）
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if file.endswith('.md'):
                    md_files.append(Path(root) / file)

        return md_files

    def sync_project(self, project_name: str, project_path: str, subdir: str) -> Dict:
        """同步单个项目到 Obsidian"""
        result = {
            'name': project_name,
            'subdir': subdir,
            'total': 0,
            'copied': 0,
            'updated': 0,
            'skipped': 0,
            'errors': []
        }

        # 目标目录 - 使用子目录名
        target_dir = self.obsidian_path / subdir if subdir else self.obsidian_path
        target_dir.mkdir(parents=True, exist_ok=True)

        # 查找 md 文件
        md_files = self.find_md_files(project_path)
        result['total'] = len(md_files)

        for src_file in md_files:
            try:
                # 计算相对路径，保持目录结构
                rel_path = src_file.relative_to(Path(project_path))
                target_file = target_dir / rel_path

                # 确保目标目录存在
                target_file.parent.mkdir(parents=True, exist_ok=True)

                # 检查是否需要复制
                should_copy = True
                if target_file.exists():
                    # 比较修改时间
                    if src_file.stat().st_mtime <= target_file.stat().st_mtime:
                        should_copy = False
                        result['skipped'] += 1

                if should_copy:
                    shutil.copy2(src_file, target_file)
                    if target_file.exists():
                        result['updated'] += 1
                    else:
                        result['copied'] += 1

            except Exception as e:
                result['errors'].append(f"{src_file.name}: {str(e)}")

        return result

    def sync_all(self, projects: List[Dict]) -> List[Dict]:
        """同步所有项目"""
        results = []
        for project in projects:
            subdir = project.get('subdir', '')
            result = self.sync_project(project['name'], project['path'], subdir)
            results.append(result)
        return results
