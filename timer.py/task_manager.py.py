import json
from dataclasses import dataclass
from typing import List

@dataclass
class Task:
    """任务类"""
    name: str
    duration: int  # 持续时间（秒）
    description: str = ""

class TaskManager:
    """任务管理器"""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self.current_task_index = 0
        
    def add_task(self, name, duration, description=""):
        """添加任务"""
        task = Task(name, duration, description)
        self.tasks.append(task)
        
    def remove_task(self, index):
        """移除任务"""
        if 0 <= index < len(self.tasks):
            return self.tasks.pop(index)
        return None
        
    def update_task(self, index, name=None, duration=None, description=None):
        """更新任务"""
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            if name is not None:
                task.name = name
            if duration is not None:
                task.duration = duration
            if description is not None:
                task.description = description
            return True
        return False
        
    def get_total_duration(self):
        """获取总持续时间"""
        return sum(task.duration for task in self.tasks)
        
    def get_task_list(self):
        """获取任务列表"""
        return self.tasks.copy()
        
    def clear_tasks(self):
        """清空任务"""
        self.tasks.clear()
        
    def move_task_up(self, index):
        """上移任务"""
        if index > 0 and index < len(self.tasks):
            self.tasks[index], self.tasks[index-1] = self.tasks[index-1], self.tasks[index]
            return True
        return False
        
    def move_task_down(self, index):
        """下移任务"""
        if index >= 0 and index < len(self.tasks) - 1:
            self.tasks[index], self.tasks[index+1] = self.tasks[index+1], self.tasks[index]
            return True
        return False
        
    def export_to_dict(self):
        """导出为字典"""
        return {
            "tasks": [
                {
                    "name": task.name,
                    "duration": task.duration,
                    "description": task.description
                }
                for task in self.tasks
            ]
        }
        
    def import_from_dict(self, data):
        """从字典导入"""
        self.tasks.clear()
        for task_data in data.get("tasks", []):
            self.add_task(
                task_data["name"],
                task_data["duration"],
                task_data.get("description", "")
            )