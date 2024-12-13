import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
import queue
import time
import task

# 锁对象，确保线程安全
lock = task.lock


def run_worker():
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
        # 提交任务到线程池
        while True:
            # 检查线程池是否有空闲线程
            if executor._work_queue.qsize() < 1:
                # 提交任务到线程池
                executor.submit(run_task)
            
            
            time.sleep(task.NEXT_DELAY)  # 延迟后提交下一个任务
            


# 执行任务的函数
def run_task():
    try:
        # 取出任务参数
        args = next(task.params)
        result = task.main(*args)

    except Exception as e:
        print(f"Error occurred in task : {e}\nargs: {args}\n")

# 监视线程的函数
def run_monitor():
    while True:
        task.monitor()
        time.sleep(task.MONITOR_INTERVAL)



def main():
    thread_worker = threading.Thread(target=run_worker,daemon=True)
    thread_worker.start()
    print('start thread_worker')

    thread_monitor = threading.Thread(target=run_monitor,daemon=True)
    thread_monitor.start()
    print('start thread_monitor')

    while True:
        input()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n>> Interrupt <<  ')
        os.abort()
