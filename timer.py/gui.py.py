import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from timer import Timer
from task_manager import TaskManager
from csv_handler import CSVHandler

class TimerGUI:
    """计时器图形界面"""
    
    def __init__(self, timer, task_manager, csv_handler):
        self.timer = timer
        self.task_manager = task_manager
        self.csv_handler = csv_handler
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("团队会议倒计时器")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 状态变量
        self.is_running = False
        self.is_paused = False
        
        # 创建界面
        self._create_widgets()
        
        # 注册计时器回调
        self.timer.add_callback(self._update_timer_display)
        
    def _create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 计时器显示
        self.time_label = tk.Label(main_frame, text="00:00", font=("Arial", 24))
        self.time_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # 控制按钮框架
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        self.start_button = ttk.Button(control_frame, text="开始", command=self._start_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = ttk.Button(control_frame, text="暂停", command=self._pause_timer, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="停止", command=self._stop_timer, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # 任务管理框架
        task_frame = ttk.LabelFrame(main_frame, text="会议议程管理", padding="5")
        task_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        task_frame.columnconfigure(1, weight=1)
        
        # 任务列表
        self.task_tree = ttk.Treeview(task_frame, columns=("Duration", "Description"), show="headings", height=8)
        self.task_tree.heading("#0", text="任务名称")
        self.task_tree.heading("Duration", text="持续时间(秒)")
        self.task_tree.heading("Description", text="描述")
        self.task_tree.column("#0", width=200)
        self.task_tree.column("Duration", width=100)
        self.task_tree.column("Description", width=200)
        self.task_tree.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 任务操作按钮
        ttk.Button(task_frame, text="添加任务", command=self._add_task_dialog).grid(row=1, column=0, padx=2, pady=5)
        ttk.Button(task_frame, text="编辑任务", command=self._edit_task_dialog).grid(row=1, column=1, padx=2, pady=5)
        ttk.Button(task_frame, text="删除任务", command=self._delete_task).grid(row=1, column=2, padx=2, pady=5)
        ttk.Button(task_frame, text="清空任务", command=self._clear_tasks).grid(row=1, column=3, padx=2, pady=5)
        
        # 文件操作框架
        file_frame = ttk.LabelFrame(main_frame, text="文件操作", padding="5")
        file_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(file_frame, text="导入CSV", command=self._import_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="导出CSV", command=self._export_csv).pack(side=tk.LEFT, padx=5)
        
        # 时间调整框架
        adjust_frame = ttk.LabelFrame(main_frame, text="时间调整", padding="5")
        adjust_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(adjust_frame, text="+1分钟", command=lambda: self._adjust_time(60)).pack(side=tk.LEFT, padx=5)
        ttk.Button(adjust_frame, text="+5分钟", command=lambda: self._adjust_time(300)).pack(side=tk.LEFT, padx=5)
        ttk.Button(adjust_frame, text="-1分钟", command=lambda: self._adjust_time(-60)).pack(side=tk.LEFT, padx=5)
        ttk.Button(adjust_frame, text="-5分钟", command=lambda: self._adjust_time(-300)).pack(side=tk.LEFT, padx=5)
        
        # 配置网格权重
        main_frame.rowconfigure(2, weight=1)
        task_frame.rowconfigure(0, weight=1)
        task_frame.columnconfigure(0, weight=1)
        
    def _update_task_display(self):
        """更新任务列表显示"""
        # 清空现有显示
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
            
        # 添加任务到列表
        for i, task in enumerate(self.task_manager.get_task_list()):
            minutes = task.duration // 60
            seconds = task.duration % 60
            duration_text = f"{minutes}:{seconds:02d}"
            self.task_tree.insert("", "end", text=task.name, values=(duration_text, task.description))
            
    def _add_task_dialog(self):
        """添加任务对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加任务")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="任务名称:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(dialog, width=20)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Label(dialog, text="分钟:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        minutes_spinbox = tk.Spinbox(dialog, from_=0, to=120, width=5)
        minutes_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(dialog, text="秒:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        seconds_spinbox = tk.Spinbox(dialog, from_=0, to=59, width=5)
        seconds_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(dialog, text="描述:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        desc_entry = ttk.Entry(dialog, width=20)
        desc_entry.grid(row=3, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        def add_task():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("错误", "请输入任务名称")
                return
                
            try:
                minutes = int(minutes_spinbox.get())
                seconds = int(seconds_spinbox.get())
                total_seconds = minutes * 60 + seconds
                
                if total_seconds <= 0:
                    messagebox.showerror("错误", "持续时间必须大于0")
                    return
                    
                self.task_manager.add_task(name, total_seconds, desc_entry.get())
                self._update_task_display()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
                
        ttk.Button(dialog, text="添加", command=add_task).grid(row=4, column=0, columnspan=2, pady=10)
        
        dialog.columnconfigure(1, weight=1)
        
    def _edit_task_dialog(self):
        """编辑任务对话框"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个任务")
            return
            
        index = self.task_tree.index(selection[0])
        task = self.task_manager.get_task_list()[index]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑任务")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="任务名称:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(dialog, width=20)
        name_entry.insert(0, task.name)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        minutes = task.duration // 60
        seconds = task.duration % 60
        
        ttk.Label(dialog, text="分钟:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        minutes_spinbox = tk.Spinbox(dialog, from_=0, to=120, width=5)
        minutes_spinbox.delete(0, tk.END)
        minutes_spinbox.insert(0, str(minutes))
        minutes_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(dialog, text="秒:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        seconds_spinbox = tk.Spinbox(dialog, from_=0, to=59, width=5)
        seconds_spinbox.delete(0, tk.END)
        seconds_spinbox.insert(0, str(seconds))
        seconds_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(dialog, text="描述:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        desc_entry = ttk.Entry(dialog, width=20)
        desc_entry.insert(0, task.description)
        desc_entry.grid(row=3, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        def update_task():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("错误", "请输入任务名称")
                return
                
            try:
                minutes = int(minutes_spinbox.get())
                seconds = int(seconds_spinbox.get())
                total_seconds = minutes * 60 + seconds
                
                if total_seconds <= 0:
                    messagebox.showerror("错误", "持续时间必须大于0")
                    return
                    
                self.task_manager.update_task(index, name, total_seconds, desc_entry.get())
                self._update_task_display()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
                
        ttk.Button(dialog, text="更新", command=update_task).grid(row=4, column=0, columnspan=2, pady=10)
        
        dialog.columnconfigure(1, weight=1)
        
    def _delete_task(self):
        """删除选中任务"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个任务")
            return
            
        if messagebox.askyesno("确认"", ""确定要删除这个任务吗")