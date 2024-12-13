from collections import Counter, deque
from itertools import count
import time
import threading
from typing import Deque
import fetch

# 配置参数
MAX_CONCURRENT = 125  # 最大并发数量
NEXT_DELAY = 5 # 每次创建新任务的间隔（秒）
MONITOR_INTERVAL = 1  # 监视线程刷新间隔（秒）


MONITOR_RESULT_COUNT = 10  # 最近完成任务结果的记录数量
MONITOR_HANDLE_COUNT = 10  # 最近启动任务的记录数量

results:Deque[fetch.Fetch] = deque(maxlen=MONITOR_RESULT_COUNT)  # 最近完成任务的结果（固定长度）
handles:Deque[fetch.Fetch] = deque(maxlen=MONITOR_HANDLE_COUNT)
cnt = Counter()
lock = threading.Lock()  # 锁保护共享数据

def main(url, note):
    f = fetch.Fetch(url, note)

    with lock:
        handles.append(f)
        cnt['req'] += 1
        cnt['fetching'] += 1

    f.run()

    with lock:
        cnt['fetching'] -= 1
        cnt['res'] += 1

        if f in handles:
            handles.remove(f)
        results.append(f) 

    if f.error:
        return str(f.error)
    
    return f
    


def monitor():
    text = ''
    text += "-- Monitoring -- \n"
    if cnt['res']:
        for i, endf in enumerate(results, 1):
            text += (f"{i}: {endf.report()}\n")
    else:
        text += ("No results.\n")

    text += "-- Running -- \n"
    if cnt['fetching']:
        for  f in handles:
            text += (f"{f.see()}\n")
    else:
        text += ("No fetching.\n")

    # 帮我完成这个函数
    t = int(time.time() - init_time)
    text += f'alive: {t}s  req:{cnt["req"]} \n' 
    print(text)

        

def param_generator():
    for i in count(1):  # 从 1 开始无限计数
        url = f'http://speedtest4.tele2.net/1GB.zip?q={i}'
        note = f'URL_{i}'
        yield (url, note)

params = param_generator()

init_time = time.time()

if __name__ == "__main__":

    while True:
        main(*next(params))
        monitor()
        time.sleep(1)


