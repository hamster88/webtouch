from collections import Counter, deque
from itertools import count
import time
import threading
from typing import Deque
from webtouch import fetch


class Options:
    url:str = 'http://speedtest4.tele2.net/1GB.zip?q={}'
    concurrent:int = 32
    delay:list[float] = [5,5]
    watch:int = 10
    interpolation:list[int] = []


opts:Options = Options()

def init(new_options):
    global opts,results,handles,errors,params
    opts = new_options

    params = param_generator(opts.url, opts.interpolation)
    results = deque(maxlen=opts.watch) 
    handles = deque(maxlen=opts.concurrent)
    errors = deque(maxlen=opts.watch)
    



# 配置参数
MONITOR_INTERVAL = 1  # 监视线程刷新间隔（秒）

results:Deque[fetch.Fetch] = deque(maxlen=opts.watch)  # 最近完成任务的结果（固定长度）
handles:Deque[fetch.Fetch] = deque(maxlen=opts.concurrent)
errors:Deque[fetch.Fetch] = deque(maxlen=opts.watch)
cnt = Counter()
lock = threading.Lock()  # 锁保护共享数据

def main(url, note):
    f = fetch.Fetch(url, note)

    with lock:
        handles.append(f)
        cnt['total'] += 1
        cnt['alive'] += 1
        f.id = str(cnt['total'])

    f.run()

    with lock:
        cnt['alive'] -= 1
        cnt['done'] += 1

        if f in handles:
            handles.remove(f)


        if f.error:
            errors.append(f)
            cnt['error'] += 1
        else:
            results.append(f) 
            cnt['res'] += 1

        
    
    return f
    


def monitor():
    text = ''

    text += "-------------- \n"
    text += f"Result({cnt['res']})  Error({cnt['error']})\n"
    if cnt['error']:
        for ef in errors:
            text += (f"{ef.id}: {ef.report()}\n")
    if cnt['res']:
        for rf in results:
            text += (f"{rf.id}: {rf.report()}\n")
    else:
        text += ("No results.\n")

    text += "-- Running ---- \n"
    if cnt['alive']:
        with lock:
            left, right, n_skip = my_slice(handles, opts.watch)
        for  f in left:
            text += (f"{f.id}: {f.see()}\n")
        if n_skip:
            text += f'     ...{n_skip}\n'
        for  f in right:
            text += (f"{f.id}: {f.see()}\n")
    else:
        text += ("No alive.\n")

    t = int(time.time() - init_time)
    clock =  time.strftime("%H:%M:%S", time.gmtime(t))
    text += f'{clock}  alive: {cnt["alive"]}  total: {cnt["total"]} \n' 
    print(text)

        

def param_generator(url_template:str, interpolation_modes=[]):
    for i in count(1):  
        # TODO: interpolations = next(iter_interpolations)
        interpolations = (i,)
        url = url_template.format(*interpolations)
        note = '_'.join(['URL',*[str(x) for x in interpolations]])
        yield (url, note)

params = param_generator(opts.url)


def clear_error():
    with lock:
        errors.clear()

def my_slice(arr, n):
    a = list(arr)
    if len(a) < n:
        return a, [], 0
    
    l = n // 2
    r = -(l + n % 2)

    return a[0:l], a[r:], len(a) - n




init_time = time.time()

if __name__ == "__main__":

    while True:
        main(*next(params))
        monitor()
        time.sleep(1)


