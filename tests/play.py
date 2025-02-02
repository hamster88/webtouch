print('\x1b[?25l \r', end='', flush=True)
import time
# import sys
# sys.stdout.flush()
time.sleep(2)
print('hello')
time.sleep(2)
print('\x1b[?25h', end='')
exit()

try:
    import curses
    _not_import_curses = False
except ImportError as e:
    _not_import_curses = f'''{e.__class__.__name__}: {e.msg}
    If you are using windows, please try:
        pip install windows-curses
  
    If it is not solved, please report this problem.
    '''.strip()


if _not_import_curses:
    print(_not_import_curses)
    exit(1)



    
import time

def process_logs(stdscr):
    stdscr.clear()

    height, width = stdscr.getmaxyx()
    ok_window_height = height // 2
    fail_window_height = height - ok_window_height
    ok_win = stdscr.subwin(ok_window_height, width, 0, 0)  # 上半部分
    fail_win = stdscr.subwin(fail_window_height, width, ok_window_height, 0)  # 下半部分
   
    logs = [
        "OK - Task 1 completed"*10,
        "FAIL - Task 2 failed",
        "OK - Task 3 completed",
        "FAIL - Task 4 failed",
        "OK - Task 5 completed",
        "FAIL - Task 6 failed",
    ]

    ok_logs = []
    fail_logs = []

    # 逐步处理日志流
    for log in logs:
        if log.startswith("OK"):
            ok_logs.append(log)
        elif log.startswith("FAIL"):
            fail_logs.append(log)

        # 更新 OK 窗口
        ok_win.clear()
        ok_win.addstr("OK Logs:\n", curses.color_pair(1))
        for line in ok_logs:
            ok_win.addstr(line + "\n")
        ok_win.box()

        # 更新 FAIL 窗口
        fail_win.clear()
        fail_win.addstr("FAIL Logs:\n", curses.color_pair(2))
        for line in fail_logs:
            fail_win.addstr(line + "\n")
        fail_win.box()

        # 刷新屏幕
        stdscr.refresh()
        ok_win.refresh()
        fail_win.refresh()

        # 模拟日志流的延迟
        time.sleep(1)


def curses_app(stdscr):
    # 初始化颜色对
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # OK 日志颜色
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # FAIL 日志颜色

    # 启动日志处理
    process_logs(stdscr)

# 参数设置
length = 80  # 数据点数
amplitude = 0.1  # 振幅
frequency = 15  # 波浪频率
noise_level = 2  # 随机性强度
smooth_factor = 15  # 平滑因子
seed = None  # 随机数种子（可选）



def draw_bar_chart(stdscr):
  while True:
    # 生成波浪
    wave = generate_random_wave(length=length, amplitude=amplitude, frequency=frequency, noise_level=noise_level, smooth_factor=smooth_factor, seed=seed)

    #显示波浪
    data = display_wave(wave)


    # 取消光标显示
    curses.curs_set(0)

    # 初始化颜色模式
    curses.start_color()

    # 定义自定义 RGB 颜色（支持的终端需为 xterm-256color 或更高）
    if curses.can_change_color():
        # 定义颜色编号 8 为 (255, 0, 0) 的红色
        curses.init_color(8, 1000, 0, 0)  # Red (RGB 255,0,0)
        # 定义颜色编号 9 为 (0, 255, 0) 的绿色
        curses.init_color(9, 0, 1000, 0)  # Green (RGB 0,255,0)
        # 定义颜色编号 10 为 (0, 0, 255) 的蓝色
        curses.init_color(10, 300, 300, 500)  # Blue (RGB 0,0,255)

        # 定义颜色对
        curses.init_pair(1, curses.COLOR_WHITE, 10)  # 红色背景
        curses.init_pair(2, curses.COLOR_WHITE, 10)  # 绿色背景
        curses.init_pair(3, curses.COLOR_WHITE, 10)  # 蓝色背景
    else:
        # 如果终端不支持自定义颜色，使用标准颜色
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)

    # 获取窗口大小
    height, width = stdscr.getmaxyx()

    # 确保数据量适配窗口宽度
    max_bars = width - 2  # 留出左右边界
    if len(data) > max_bars:
        data = data[:max_bars]

    # 确保柱子的高度不会超出窗口高度
    max_height = height - 2  # 可用高度，减去顶部和底部边界
    for idx, value in enumerate(data):
        # 如果数值大于窗口高度，则截断为窗口高度
        bar_height = min(value, max_height)

        # 动态选择颜色对（循环使用不同的颜色对）
        color_pair = curses.color_pair((idx % 3) + 1)
        
        
        # 从底部开始绘制柱子，逐行绘制
        for y in range(height - 2, height - 2 - bar_height, -1):
            stdscr.addstr(y, idx + 1,       " ", color_pair)  # 用动态颜色填充

    # 刷新屏幕
    stdscr.refresh()
    
    
    # 等待用户按键退出
    stdscr.getch()
    stdscr.clear()




import math
import random

def generate_random_wave(length=1000, amplitude=1, frequency=1, noise_level=0.1, smooth_factor=5, seed=None):
    """
    生成一个平滑的波浪，并带有一定的随机性。

    参数:
    length (int): 波浪的长度（数据点数）。
    amplitude (float): 波浪的最大振幅。
    frequency (float): 波浪的频率。
    noise_level (float): 随机噪声的强度，值越大随机性越高。
    smooth_factor (int): 平滑的随机噪声的窗口大小。
    seed (int): 随机数种子（可选，用于复现结果）。

    返回:
    list: 包含生成波浪数据的列表。
    """
    if seed is not None:
        random.seed(seed)

    # 生成时间轴（0 到 2π * frequency）
    t_values = [(2 * math.pi * frequency * i / length) for i in range(length)]

    # 生成基础波浪 (正弦波)
    base_wave = [amplitude * math.sin(t) for t in t_values]

    # 添加随机噪声
    noise = [random.uniform(-noise_level, noise_level) for _ in range(length)]

    # 平滑噪声 (使用滑动平均)
    smooth_noise = []
    for i in range(length):
        start = max(0, i - smooth_factor // 2)
        end = min(length, i + smooth_factor // 2 + 1)
        smooth_noise.append(sum(noise[start:end]) / (end - start))

    # 叠加波浪和随机噪声
    wave = [base_wave[i] + smooth_noise[i] for i in range(length)]

    return wave

# 测试和可视化
def display_wave(wave, base=10,scale=10):
    """
    打印波浪（简单可视化，使用文本输出）。
    """
    min_wave = min(wave)
    max_wave = max(wave)
    range_wave = max_wave - min_wave
    
    chert = []
    for value in wave:
        position = int((value - min_wave) / range_wave * scale)
        #line = " " * position + "*"
        #print(line)
        chert.append(position)
    return chert





# 数据
#data =[5, 5, 5, 0, 1, 2, 6, 9, 9, 6, 3, 2, 5, 9, 10, 6, 3, 2, 3, 3, 4, 3, 0, 0, 3, 4, 5, 3, 1, 1] # 每个数据点表示柱子的高度

# 运行 curses 应用程序
curses.wrapper(draw_bar_chart)


