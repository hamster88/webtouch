from collections import deque
import os
from pprint import pprint
import textwrap  
from webtouch.reporter import Reporter
from webtouch.viewer import BaseViewer


try:
    import curses
    _not_import_curses = False
except ImportError as e:
    _not_import_curses = f'''{e.__class__.__name__}: {e.msg}
    If you are using windows, please try:
        pip install windows-curses
  
    If it is not solved, please report this problem.
    '''.strip()
    
    


class CursesViewer(BaseViewer):
    def __init__(self):
        super().__init__()
        
        self.putlog = self._putlog
        self.logs = deque(maxlen=100)
        
        self.stdscr:curses.window = None
        self.my = 0
        self.mx = 0

        self.front = 'main'
        # self.front = 'log'
        
        self.run_win:curses.window = None
        self.his_win:curses.window = None
        


    def view_run(self):
        h , w = self.run_win.getmaxyx()
        
        maxyx = self.stdscr.getmaxyx()
        _debug  = f'view_main\n{self.my=} {self.mx=} {maxyx=}          '
        
        img = 'running: '
        for i in self.reporter.running:
            img += f'\n{i.tid}\t{i.title}'
        
        img = img.expandtabs(4)
        
        lines = []
        for l in img.splitlines():
            pl = f'{l:<{w-1}}'
            lines.append(pl)
            
        img = '\n'.join(lines)
        
        
        try:
            # self.run_win.clear()
            # self.run_win.addstr(0, 0, _debug)
            self.run_win.addstr(0, 0, img)
            self.run_win.refresh()
            
            # self.his_win.addstr(0, 0, '------')
            # self.his_win.addstr(1, 0, '------')
            # self.his_win.addstr(2, 0, '------')
            # self.his_win.refresh()
        except:
            pass
    
    def view_his(self):
        h , w = self.his_win.getmaxyx()
        # os.get_terminal_size()
        maxyx = self.stdscr.getmaxyx()
        _debug  = f'{h=} {w=} {self.my=}\t{self.mx=}\t'
        
        
        img = 'history: {_debug}'
        for i in list(self.reporter.history)[-h+1:]:
            img += f'\n{i.tid}\t{i.title}'
        
        lines = img.splitlines()
        
        # self.postimg(img, w)
        self.his_win.addstr(0, 0, '========')
        self.his_win.addstr(1, 0, '========')
        self.his_win.addstr(2, 0, '========')
        # self.his_win.refresh()
        
        # self.addlines(self.his_win, lines)
        

    def addlines(self, win, lines):
        try:
            win.addstr(0, 0, '????')
            
            for i  in range(lines):
                l = lines[i]
                win.addstr(i, 0, '????')
            win.refresh()
        except:
            pass
        
    def view_debug(self):
        for i in range(self.my):
            try:
                self.stdscr.addstr(i,0,str(i))
            except:
                pass
            
        for i in range(self.mx):
            try:
                self.stdscr.addstr(13,i,str(i%10))
            except:
                pass
            
        
    def handle_begin(self):
        if self.stdscr and self.front == 'main':
            self.view_run()
    
    def handle_end(self):
        if self.stdscr and self.front == 'main':
            self.view_his()
    
    def make_layout(self):
        vh = self.my
        vw = self.mx
        
        
        bh = 4
        hh = (vh - bh) // 2
        rh = vh - hh - bh
        
        
        
        self.run_win = curses.newwin(rh, vw, 0, 0)
        self.his_win = curses.newwin(hh, vw, rh, 0)
        
        if self.front == 'main':
            self.view_run()
            self.view_his()
    
    def _putlog(self, message):
        self.logs.append(message)
        
        if self.stdscr and self.front == 'log':
            self.view_logcat()
    
    def view_logcat(self):
        initial_prefix    = '* | '
        subsequent_prefix = '  | '
        max_line = self.my
        max_width = self.mx - len(initial_prefix) -1
        
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
            prefix = flag and initial_prefix or subsequent_prefix
            text_buff += f'{prefix}{line}\n'

        
        try:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, text_buff)
            self.stdscr.refresh()
        except:
            pass
        
        # maxyx = self.stdscr.getmaxyx()
        # _debug  = f'{self.my=} {self.mx=} {maxyx=}          '
        # self.stdscr.addstr(0, 0, _debug)

    def main(self, stdscr):
        # 初始化 stdscr
        self.stdscr = stdscr
        self.stdscr.clear()
        curses.curs_set(0)
        # self.my, self.mx =  self.stdscr.getmaxyx()
        self.check_resize()
        
        # 绑定数据模型事件
        self.reporter.on_begin = self.handle_begin
        self.reporter.on_end = self.handle_end
        # self.reporter.on_end
        
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
    
    def postimg(self, img:str, width:int):
        lines = []
        for l in img.expandtabs(4).splitlines():
            if len(l) > width:
                l = l[:width - 3] + '...'
            s = f'{l:<{width-1}}'
            lines.append(s)
            
        return lines
    

    def on_resize(self):
        self.make_layout()

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
     
        
        
