#!/usr/bin/env python3
"""
团队会议倒计时器 - 主程序
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from timer import Timer
from task_manager import TaskManager
from csv_handler import CSVHandler
from gui import TimerGUI

def main():
    """主函数"""
    print("团队会议倒计时器启动中...")
    
    # 初始化组件
    task_manager = TaskManager()
    csv_handler = CSVHandler()
    timer = Timer()
    
    # 启动GUI界面
    gui = TimerGUI(timer, task_manager, csv_handler)
    gui.run()

if __name__ == "__main__":
    main()