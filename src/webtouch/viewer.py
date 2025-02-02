from collections import deque

import os
from pprint import pprint
import textwrap  


try:
    import curses
    _not_import_curses = False
except ImportError as e:
    _not_import_curses = f'''{e.__class__.__name__}: {e.msg}
    If you are using windows, please try:
        pip install windows-curses
  
    If it is not solved, please report this problem.
    '''.strip()

class BaseViewer():
    def __init__(self):
        self.putlog = lambda s:None

    def show(self):
        print(f'{__class__.__name__}.show() is not implemented.')

    def loop(self):
        try:
            while True:
                input()
        except KeyboardInterrupt:
            pass
        finally:
            # os._exit(0)
            return

class NothingViewer(BaseViewer):
    def __init__(self):
        super().__init__()
    
    def show(self):
       self.loop()

class LogViewer(BaseViewer):
    def __init__(self):
        super().__init__()
        self.putlog = print
        
    def show(self):
       self.loop()


class CursesViewer(BaseViewer):
    def __init__(self):
        self.putlog = self._putlog
        self.logs = deque(maxlen=100)
        
        self.stdscr:curses.window = None
        self.my = 0
        self.mx = 0


    def _putlog(self, message):
        self.logs.append(message)
        
        if self.stdscr:
            max_line = self.my
            max_width = self.mx
            part_log = deque(maxlen=max_line)
            for i in range(len(self.logs) - 1, -1, -1):
                log = self.logs[i]
                # TODO: filter(log)
                part_log.appendleft(log)
                
                if len(part_log) == part_log.maxlen:
                    break
                
            
            lines = []
            for i in part_log:
                p = self.wrap(i, max_width)
                lines.append((True, p[0]))
                for s in p[1:]:
                    lines.append((False, s))
            
            
            
            text_buff = ''
            for flag, line in lines[max(0, len(lines)-max_line):]:
                prefix = flag and '* | ' or '  | '
                # prefix = flag and '* ' or ' '
                text_buff += f'{prefix}{line}\n'
                # for s in parag[1:]:
                #     text_buff += f'  |  {s}\n'
            
            try:
                self.stdscr.clear()
                self.stdscr.addstr(0, 0, text_buff)
                self.stdscr.refresh()
            except:
                pass
            
            # _debug  = f'{self.mx} {self.mx} '
            # self.stdscr.addstr(20, 0, _debug)
        

    def main(self, stdscr):
        # 初始化 stdscr
        self.stdscr = stdscr
        self.stdscr.clear()
        curses.curs_set(0)
        
        # 示例:显示一条消息
        self._putlog("Press any key to continue or 'q' to quit.")

        # 进入事件循环
        self.loop()
    
    def wrap(self, text:str, width):
        lines = text.splitlines()
        res = []
        for l in lines:
            res += textwrap.wrap(
                l, 
                width,                        # 每行最大宽度
                initial_indent='',            # 第一行的缩进
                subsequent_indent='',         # 后续行的缩进
                expand_tabs=True,             # 替换制表符为空格
                replace_whitespace=True,      # 替换空白字符为普通空格
                fix_sentence_endings=False,   # 修复句末空格
                break_long_words=True,        # 是否允许单词中断行
                drop_whitespace=False,        # 移除行尾多余空格
                break_on_hyphens=True,        # 连字符处是否可断行
                tabsize=4,                    # 制表符宽度
                max_lines=None,               # 限制最大行数
                placeholder=' [...]'          # 截断时使用的占位符
            )
            
        return res
    

    def on_resize(self):
        pass

    def check_resize(self):
        my, mx =  self.stdscr.getmaxyx()
        if self.mx != mx or self.my != my:
            self.my = my
            self.mx = mx
            self.on_resize()
            
    
    def show(self):
        # print('\x1b[?25l \r', end='', flush=True)
        # 使用 curses.wrapper 自动管理终端状态
        curses.wrapper(self.main)
        # print('\x1b[?25h \r', end='', flush=True)
        

    def loop(self):
        self.stdscr.timeout(100)  # 设置超时时间为 100 毫秒
       
        while True:
            try:
                ch = self.stdscr.getch()
                self.check_resize()
                if ch == curses.ERR:  # 没有按键事件
                    pass
                else:
                    self._putlog(f"You pressed: {chr(ch)} ({ch})")
            except KeyboardInterrupt:
                return
     
        
        
        
