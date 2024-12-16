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
                        help="Maximum concurrency")
    parser.add_argument("-d", "--delay", metavar='<seconds>', type=float, action="append", default=[],
                        help="Submission delay between each requested task, setting it twice indicates the delay range")
    parser.add_argument("-w", "--watch",metavar='<num>', type=int, default=app.option.watch,
                        help="Maximum count of watch")
    parser.add_argument("-i", "--interpolation", metavar='<rule>', type=str, action="append", default=[],
                        help="Rule of dynamic URL generator")
    parser.add_argument("-H", "--header", metavar='<name:value>', type=str, action="append", default=[],
                        help="Set headers")
    parser.add_argument("--cookies", metavar='<file>', type=str,
                        help="Load cookies.txt")
    


    
    args = parser.parse_args()
    if len(args.delay) == 0:
        args.delay = [5,5]
    if len(args.delay) == 1:
        args.delay *= 2
        
    if args.header:
        args.new_headers = parse_headers(args.header)
    else:
        args.new_headers = {}
        
    app.main(args)

def parse_headers(haders:list[str]) -> dict[str,str]:
    d = {}
    for h in haders:
        k, v = h.split(':', 1)
        d[k] = v
        
    return d
        
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n>> Interrupt <<  ')
        os.abort()