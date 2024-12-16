from itertools import count
import os
import random
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
import queue
import time
from pprint import pprint
from http.cookiejar import MozillaCookieJar


from webtouch import task
from webtouch import util

MONITOR_INTERVAL = 1 # 监视线程刷新间隔（秒）

lock = threading.Lock()

class TypingOption:
    url:str = 'http://speedtest4.tele2.net/1GB.zip?q={}'
    concurrent:int = 32
    delay:list[float] = [5,5]
    watch:int = 10
    interpolation:list[str] = ['1-65536']
    cookies:str = None
    new_headers:str = {}
 
option:TypingOption = TypingOption()


def param_generator(url_template:str, rules:list[str]=[]):
    interpolation_iters = util.interpolation_generator(rules)
    for i in count(1):
        interpolations = []
        notes = ['URL']
        for it in interpolation_iters:
            val = next(it)
            interpolations.append(val)
            notes.append(str(val))

        if len(notes) == 1:
            notes.append(str(i))

        url = url_template.format(*interpolations)
        note = '_'.join(notes)
        yield (url, note)

param_iter = param_generator('http://127.0.0.1:8000/api?id={}',['1-10'])


def run_worker():
    with ThreadPoolExecutor(max_workers=option.concurrent) as executor:
        # 提交任务到线程池
        while True:
            # 检查线程池是否有空闲线程
            if executor._work_queue.qsize() < 1:
                # 提交任务到线程池
                executor.submit(run_task)
            
            
            s = random.uniform(*sorted(option.delay[-2:]))
            time.sleep(s)  # 延迟后提交下一个任务



# 执行任务的函数
def run_task():
    try:
        # 取出任务参数
        with lock:
            args = next(param_iter)

        result = task.main(*args, new_headers=option.new_headers)

    except Exception as e:
        print(f"Abort task : {e}\nargs: {args}\n")

# 监视线程的函数
def run_monitor():
    while True:
        task.monitor()
        time.sleep(MONITOR_INTERVAL)



def init(new_option=None):
    global option, param_iter
    if new_option:
        option = new_option

    if option.cookies:
        # 加载 cookies.txt 文件
        cookie_jar = MozillaCookieJar(option.cookies)
        cookie_jar.load(ignore_discard=True, ignore_expires=True)
        
        task.cookie_jar = cookie_jar
        

    param_iter = param_generator(option.url, option.interpolation)
    task.init(option.watch, option.watch, option.watch, option.concurrent)

def main(args):
    print('* start pression')
    init(args)
    pprint(option)

    thread_worker = threading.Thread(target=run_worker,daemon=True)
    thread_worker.start()
    print('* start thread_worker')

    thread_monitor = threading.Thread(target=run_monitor,daemon=True)
    thread_monitor.start()
    print('* start thread_monitor')

    try:
        while True:
            input()
            task.clear_error()
            print('* cleared error message.')
            pprint(option)

    except KeyboardInterrupt:
        print('\n>> Interrupt <<  ')
        os.abort()


