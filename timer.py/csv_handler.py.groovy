import csv
import os
from task_manager import TaskManager

class CSVHandler:
    """CSV文件处理器"""
    
    @staticmethod
    def export_to_csv(task_manager, filename):
        """导出任务到CSV文件"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # 写入表头
                writer.writerow(['Task Name', 'Duration (seconds)', 'Description'])
                
                # 写入任务数据
                for task in task_manager.get_task_list():
                    writer.writerow([task.name, task.duration, task.description])
                    
            return True, f"成功导出到 {filename}"
        except Exception as e:
            return False, f"导出失败: {str(e)}"
            
    @staticmethod
    def import_from_csv(task_manager, filename):
        """从CSV文件导入任务"""
        if not os.path.exists(filename):
            return False, f"文件不存在: {filename}"
            
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                task_manager.clear_tasks()
                
                for row in reader:
                    name = row.get('Task Name', '').strip()
                    duration_str = row.get('Duration (seconds)', '0').strip()
                    description = row.get('Description', '').strip()
                    
                    # 验证数据
                    if not name:
                        continue
                        
                    try:
                        duration = int(duration_str)
                        if duration <= 0:
                            continue
                    except ValueError:
                        continue
                        
                    task_manager.add_task(name, duration, description)
                    
            return True, f"成功从 {filename} 导入"
        except Exception as e:
            return False, f"导入失败: {str(e)}"
            
    @staticmethod
    def validate_csv_format(filename):
        """验证CSV文件格式"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                required_columns = ['Task Name', 'Duration (seconds)']
                
                if not all(col in reader.fieldnames for col in required_columns):
                    return False, "CSV文件缺少必要的列"
                    
                return True, "CSV格式正确"
        except Exception as e:
            return False, f"文件读取错误: {str(e)}"