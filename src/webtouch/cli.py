import argparse

import app

def main():
    app.main()
    return 
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description="一个简单的CLI计算器")

    # 添加参数
    parser.add_argument("num1", type=float, help="第一个数字")
    parser.add_argument("num2", type=float, help="第二个数字")
    parser.add_argument("-a", "--add", action="store_true", help="执行加法操作")
    parser.add_argument("-s", "--subtract", action="store_true", help="执行减法操作")
    parser.add_argument("-m", "--multiply", action="store_true", help="执行乘法操作")
    parser.add_argument("-d", "--divide", action="store_true", help="执行除法操作")

    # 解析命令行参数
    args = parser.parse_args()

    # 根据用户输入执行对应的操作
    if args.add:
        print(f"结果: {args.num1} + {args.num2} = {args.num1 + args.num2}")
    elif args.subtract:
        print(f"结果: {args.num1} - {args.num2} = {args.num1 - args.num2}")
    elif args.multiply:
        print(f"结果: {args.num1} * {args.num2} = {args.num1 * args.num2}")
    elif args.divide:
        if args.num2 != 0:
            print(f"结果: {args.num1} / {args.num2} = {args.num1 / args.num2}")
        else:
            print("错误: 除数不能为0")
    else:
        print("错误: 请指定一个操作 (例如: -a, -s, -m, -d)")

if __name__ == "__main__":
    main()