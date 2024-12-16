from collections import Counter, deque
import time
import threading
from typing import Deque
from webtouch import fetch




def init(watch_size=10, results_size=10, errors_size=10, handles_size=1024):
    '''
    初始化任务参数
    '''
    global results, handles, errors, n_watch

    n_watch = watch_size
    errors = deque(maxlen=errors_size)
    results = deque(maxlen=results_size) 
    handles = deque(maxlen=handles_size)
    
# 记录完成请求的结果
errors:Deque[fetch.Fetch] = deque(maxlen=5)
results:Deque[fetch.Fetch] = deque(maxlen=5) 

# 记录正在执行的请求
handles:Deque[fetch.Fetch] = deque(maxlen=255)
n_watch = 10 # 监视正在执行的请求

cnt = Counter()  # 统计数据
lock = threading.Lock()  # 锁保护共享数据

cookie_jar=None
max_download_bytes=1024**2

def main(url, note, new_headers={}):
    '''
    单个请求任务
    '''

    f = fetch.Fetch(url, note, cookie_jar=cookie_jar, new_headers=new_headers)

    with lock:
        handles.append(f)
        cnt['total'] += 1
        cnt['alive'] += 1
        f.id = str(cnt['total'])

    f.run()

    with lock:
        cnt['alive'] -= 1
        cnt['done'] += 1
        cnt['time'] += f.elapsed_time()

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
    if n_watch > 0:
        if cnt['error']:
            for ef in errors:
                text += (f"{ef.id}: {ef.report()}\n")
        if cnt['res']:
            for rf in results:
                text += (f"{rf.id}: {rf.report()}\n")
        else:
            text += ("No results.\n")

    if n_watch > 0:
        text += "-- Running ---- \n"
        if cnt['alive']:
            with lock:
                left, right, n_skip = my_slice(handles, n_watch)
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
    text += f'{clock}  alive: {cnt["alive"]}  total: {cnt["total"]} ({int(cnt["time"])}s) \n' 
    print(text)

        



# params = param_generator('http://127.0.0.1/')


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




