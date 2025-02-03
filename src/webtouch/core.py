from __future__ import annotations

from collections import defaultdict, deque
from queue import Queue
import logging
import threading
import time
import os
import sys

from webtouch.reporter import Reporter
from webtouch.task import Task
from webtouch.worker import Worker
import webtouch.viewer as viewer_mod

class LogHandler(logging.Handler):
    def __init__(self, on_log:callable):
        super().__init__()
        self.on_log = on_log

    def emit(self, record:logging.LogRecord):
        if not( self.on_log is None ):

            self.on_log(record)

class CoreOption():
    def __init__(self):
        self.view = 'curses'
        


class CoreApp():
    def __init__(self):
        self._key = f'Core.{hex(id(self))[2:]}'
        self.logger = logging.getLogger(self._key)
        
        self.option = CoreOption()
        self.lock = threading.Lock()
        self.viewer = self.get_viewer()
        self.savelog = None
        
        self.init_logger()
    
    def get_viewer(self):
        v = self.option.view 
        if v == 'log':
            return viewer_mod.LogViewer()
        
        if v == 'curses':
            return viewer_mod.CursesViewer()
        
        if v is None or v in ['silent', 'nothing', 'none', 'None','null']:
            return viewer_mod.NothingViewer()
        
    
    def init_logger(self):
        log_level = logging.DEBUG
        
        #长格式用于保存， 短格式用于显示
        log_format = '%(asctime)s.%(msecs)03d %(name)s [%(levelname)s] \t %(message)s'
        log_format_short = '%(asctime)s [%(levelname)s] \t %(message)s'
        
        log_datefmt = "%Y-%m-%d %H:%M:%S"
        log_datefmt_short = "%H:%M:%S"   
        
        
        # 创建日志记录器

        self.logger.setLevel(log_level)

        # 创建格式化器
        self._log_formatter = logging.Formatter(log_format, datefmt=log_datefmt)
        self._log_formatter_short = logging.Formatter(log_format_short, datefmt=log_datefmt_short)

        # 添加自定义日志处理器
        log_handler = LogHandler(self.handle_log)
        log_handler.setFormatter(self._log_formatter)
        self.logger.addHandler(log_handler)
        
        
    # 定义日志处理函数
    def handle_log(self, record: logging.LogRecord):
        
        text = self._log_formatter_short.format(record)
        text = text.replace('\n','\n  ')
        with self.lock:
            self.viewer.putlog(text)
    

    def main(self, task_cls:type[Task]): 
        self.task_cls = task_cls
        
        self.reporter = Reporter(self.task_cls.CONCURRENT)
        self.worker = Worker(self.task_cls, self.reporter)
        
        self.reporter.logger =  self.logger
        self.worker.logger =  self.logger
        self.task_cls.logger = self.logger
        
        self.worker.start()
        
        
        self.viewer.reporter = self.reporter
        self.viewer.show()

        os._exit(0)
        
        
    # def viewer(self):
        
    #     mode = self.option.view
    #     self.logger.info(f'start viewer ({mode=})')
        
    #     if mode == 'curses':
    #         pass
        
    #     if mode == 'log':
    #         try:
    #             while True:
    #                 input()
    #         except KeyboardInterrupt:
    #             pass
    #         finally:
    #             os._exit(0)
                