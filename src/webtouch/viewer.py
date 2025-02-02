from collections import deque
import os


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

# 这代码疑似内存溢出    
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
            max_line = 10
            _a = 0
            part_log = deque(maxlen=max_line)
            for i in range(len(self.logs) - 1, -1, -1):
                _a += 1
                log = self.logs[i]
                # TODO: filter(log)
                part_log.appendleft(log)
                
                if len(part_log) == part_log.maxlen:
                    break
                
            
            lines = []
            for i in part_log:
                p = self.typeset(i)
                lines.append((True, p[0]))
                for s in p[1:]:
                    lines.append((False, s))
            
            # for flag, text in lines[max(0, len(lines)-max_line):]:
            #     text = '* | '+ text
                
            #     self.stdscr.addstr(0, 0, text)
            #     self.stdscr.refresh()
            
            #这段没有被执行
            _debug = f'{len(self.logs)} {len(part_log)} {part_log.maxlen} {_a=}'
            self.stdscr.addstr(20, 0, _debug)
            self.stdscr.addstr(21, 0, message)
            

    def main(self, stdscr):
        # 初始化 stdscr
        self.stdscr = stdscr
        self.stdscr.clear()
        curses.curs_set(0)
        
        # 示例:显示一条消息
        self._putlog("Press any key to continue or 'q' to quit.")

        # 进入事件循环
        self.loop()
    
    
    
    def typeset(self, text, width=0) -> list[list]:
        width = width or self.mx
        
        lines = text.split('\n')  
        p = []
        for l in lines:
            wrapped = self.wrap_line(l, width)
            p.append(wrapped)
        return p
    
    def wrap_line(self, line, max_width):
        wrapped_lines = []
        while len(line) > max_width:
            wrapped_lines.append(line[:max_width])
            line = line[max_width:]
        wrapped_lines.append(line)
        return wrapped_lines

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
        try:
            while True:
                ch = self.stdscr.getch()
                self.check_resize()
                if ch == curses.ERR:  # 没有按键事件
                    continue
                elif ch == ord('q'):  # 如果按下 'q' 键,退出
                    break
                else:
                    self._putlog(f"You pressed: {chr(ch)}")
        except KeyboardInterrupt:
            pass
        finally:
            # self.stdscr.addstr(1, 0, "Exiting...")
            # self.stdscr.refresh()
            return 
        
        
        
