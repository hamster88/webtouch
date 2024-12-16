import argparse
import os
from pprint import pprint

from webtouch import app

def main():
    parser = argparse.ArgumentParser(prog='webtouch',description="App for processing tasks with options.")
    
    # 定义位置参数 url
    parser.add_argument("url", help="The URL to process")
    
    # 定义选项参数
    parser.add_argument("-c", "--concurrent", metavar='<num>', type=int, default=app.option.concurrent,
                        help="最大并发数(default: 32)")
    parser.add_argument("-d", "--delay", metavar='<seconds>', type=float, action="append", default=[],
                        help="提交延迟 (default: 5). 此选项可使用2次，记录到数组")
    parser.add_argument("-w", "--watch",metavar='<num>', type=int, default=app.option.watch,
                        help="监视的条目数 (default: 10)")
    parser.add_argument("-i", "--interpolation", metavar='<rule>', type=str, action="append", default=[],
                        help="Rule of dynamic URL generator")
    parser.add_argument("--cookies", metavar='<file>', type=str,
                        help="load cookies.txt")
    


    
    args = parser.parse_args()
    if len(args.delay) == 0:
        args.delay = [5,5]
    if len(args.delay) == 1:
        args.delay *= 2
    
    app.main(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n>> Interrupt <<  ')
        os.abort()