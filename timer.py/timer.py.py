import threading
import time
from datetime import datetime, timedelta

class Timer:
    """计时器类"""
    
    def __init__(self):
        self.is_running = False
        self.is_paused = False
        self.remaining_time = 0  # 剩余时间（秒）
        self.total_time = 0
        self.current_task_index = 0
        self.start_time = None
        self.pause_time = None
        self.callbacks = []
        
    def start(self, total_seconds):
        """开始计时"""
        self.total_time = total_seconds
        self.remaining_time = total_seconds
        self.is_running = True
        self.is_paused = False
        self.start_time = datetime.now()
        self._run_timer()
        
    def pause(self):
        """暂停计时"""
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.pause_time = datetime.now()
            
    def resume(self):
        """恢复计时"""
        if self.is_running and self.is_paused:
            self.is_paused = False
            # 调整开始时间以补偿暂停时间
            pause_duration = (datetime.now() - self.pause_time).total_seconds()
            self.start_time += timedelta(seconds=pause_duration)
            self.pause_time = None
            
    def stop(self):
        """停止计时"""
        self.is_running = False
        self.is_paused = False
        
    def add_time(self, seconds):
        """增加时间"""
        if self.is_running:
            self.total_time += seconds
            self.remaining_time += seconds
            
    def subtract_time(self, seconds):
        """减少时间"""
        if self.is_running and self.remaining_time > seconds:
            self.total_time -= seconds
            self.remaining_time -= seconds
            
    def _run_timer(self):
        """计时器线程"""
        def timer_loop():
            while self.is_running and self.remaining_time > 0:
                if not self.is_paused:
                    self.remaining_time = self.total_time - (datetime.now() - self.start_time).total_seconds()
                    if self.remaining_time <= 0:
                        self.remaining_time = 0
                        self.is_running = False
                        self._notify_time_up()
                    else:
                        self._notify_tick()
                time.sleep(0.1)
                
        thread = threading.Thread(target=timer_loop)
        thread.daemon = True
        thread.start()
        
    def add_callback(self, callback):
        """添加回调函数"""
        self.callbacks.append(callback)
        
    def _notify_tick(self):
        """通知时间更新"""
        for callback in self.callbacks:
            callback(self.remaining_time, self.total_time)
            
    def _notify_time_up(self):
        """通知时间到"""
        for callback in self.callbacks:
            if hasattr(callback, '__call__'):
                # 假设回调函数可以接受不同参数
                try:
                    callback("TIME_UP")
                except:
                    callback()
                    
    def get_formatted_time(self):
        """获取格式化时间"""
        minutes = int(self.remaining_time // 60)
        seconds = int(self.remaining_time % 60)
        return f"{minutes:02d}:{seconds:02d}"