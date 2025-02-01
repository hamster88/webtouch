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
    
print(_not_import_curses)


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

# 实现多行日志滚动显示
# * | log1 line1 loooooooooooooooooooooooo
#   | ooooooooooog texts
#   | log1 line2
# * | log2 line1 ...
class CursesViewer(BaseViewer):
    def __init__(self):
        self.stdscr:curses.window = None
        self.putlog = self._putlog
        

    def _putlog(self, message):
        text = '* | '+ message
        # 示例:在窗口中打印日志
        
        if self.stdscr:
            self.stdscr.addstr(0, 0, message)
            self.stdscr.refresh()

    def main(self, stdscr):
        # 初始化 stdscr
        self.stdscr = stdscr
        self.stdscr.clear()
        
        # 示例:显示一条消息
        self._putlog("Press any key to continue or 'q' to quit.")

        # 进入事件循环
        self.loop()

    def show(self):
        # 使用 curses.wrapper 自动管理终端状态
        curses.wrapper(self.main)

    def loop(self):
        self.stdscr.timeout(100)  # 设置超时时间为 100 毫秒
        try:
            while True:
                ch = self.stdscr.getch()
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
        
        
        

class ________CursesViewer:
    def __init__(self):
        self.stdscr: curses.window = None
        self.putlog = self._putlog
        self.log_lines = []  # 存储所有日志行
        self.max_lines = 0  # 窗口最大行数

    def _putlog(self, message):
        # 将传入的日志分割成多行后存储
        wrapped_lines = self._wrap_text('* | ' + message)
        self.log_lines.extend(wrapped_lines)

        # 如果日志行数超过屏幕高度,移除顶部多余的行(滚动效果)
        while len(self.log_lines) > self.max_lines:
            self.log_lines.pop(0)

        # 清屏并重新绘制所有日志
        self.stdscr.clear()
        for idx, line in enumerate(self.log_lines):
            self.stdscr.addstr(idx, 0, line)
        self.stdscr.refresh()

    def _wrap_text(self, text):
        """
        将长文本按窗口宽度自动换行。
        """
        max_width = self.stdscr.getmaxyx()[1] - 1  # 获取窗口宽度
        wrapped_lines = []
        while len(text) > max_width:
            wrapped_lines.append(text[:max_width])
            text = text[max_width:]
        wrapped_lines.append(text)
        return wrapped_lines

    def main(self, stdscr):
        # 初始化 stdscr
        self.stdscr = stdscr
        self.stdscr.clear()
                # 取消光标显示
        curses.curs_set(False)
        # curs_set
        # 设置窗口的最大可用行数
        self.max_lines = self.stdscr.getmaxyx()[0] - 1

        # 显示初始消息
        self._putlog("Press any key to log a message or 'q' to quit.")

        # 进入事件循环
        self.loop()

    def show(self):

        # 使用 curses.wrapper 自动管理终端状态
        curses.wrapper(self.main)

    def loop(self):
        self.stdscr.timeout(100)  # 设置超时时间为 100 毫秒
        try:
            while True:
                ch = self.stdscr.getch()
                if ch == curses.ERR:  # 没有按键事件
                    continue
                elif ch == ord('q'):  # 如果按下 'q' 键,退出
                    break
                else:
                    self._putlog(f"You pressed: {chr(ch)}")
        except KeyboardInterrupt:
            pass
        finally:
            return
