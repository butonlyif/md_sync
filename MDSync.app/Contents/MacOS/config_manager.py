import json
import os
from pathlib import Path

class ConfigManager:
    """配置管理器，负责读取和保存配置"""

    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)
        self.config = self.load_config()

    def load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.get_default_config()

    def get_default_config(self):
        """获取默认配置"""
        return {
            "obsidian_path": "",
            "projects": []
        }

    def save_config(self):
        """保存配置到文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def set_obsidian_path(self, path):
        """设置 Obsidian 路径"""
        self.config['obsidian_path'] = path
        self.save_config()

    def add_project(self, name, path, subdir):
        """添加项目"""
        # 检查是否已存在
        for project in self.config['projects']:
            if project['name'] == name:
                return False

        self.config['projects'].append({
            "name": name,
            "path": path,
            "subdir": subdir
        })
        self.save_config()
        return True

    def remove_project(self, name):
        """删除项目"""
        self.config['projects'] = [
            p for p in self.config['projects'] if p['name'] != name
        ]
        self.save_config()

    def get_projects(self):
        """获取所有项目"""
        return self.config['projects']

    def get_obsidian_path(self):
        """获取 Obsidian 路径"""
        return self.config['obsidian_path']
