import argparse
import os

from webtouch import app
from webtouch import task

def main():
    parser = argparse.ArgumentParser(prog='webtouch',description="App for processing tasks with options.")
    
    # 定义位置参数 url
    parser.add_argument("url", nargs="?", default=task.opts.url, help="The URL to process (optional).")
    
    # 定义选项参数
    parser.add_argument("-c", "--concurrent", type=int, default=task.opts.concurrent,
                        help="最大并发数")
    parser.add_argument("-d", "--delay", type=float, action="append", default=[],
                        help="提交延迟 (default: 5). 此选项可使用2次，记录到数组")
    parser.add_argument("-w", "--watch", type=int, default=task.opts.watch,
                        help="监视的条目数 (default: 10)")
    parser.add_argument("-i", "--interpolation", type=int, action="append", default=[],
                        help="设置插值的模式. 此选项可使用多次，记录到数组")
    
    args = parser.parse_args()
    if len(args.delay) == 0:
        args.delay = [5,5]
    if len(args.delay) == 1:
        args.delay *= 2
    
    app.main(args)
    # 输出解析后的参数
    # print("Parsed Arguments:")
    # print(f"URL: {args.url}")
    # print(f"Concurrent: {args.concurrent}")
    # print(f"Delay: {args.delay}")
    # print(f"Watch: {args.watch}")
    # print(f"Interpolation: {args.interpolation}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n>> Interrupt <<  ')
        os.abort()