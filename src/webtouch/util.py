import random
import sys
MAXINT = 2**31 - 1

def interpolation_generator(rules:list[str]):
    iters = []
    for rule in rules:

        try:
            int(rule)
            iters.append(gen_randint('0-'+rule))
            continue
        except ValueError:
            pass

        if '-' in rule:
            try:
                gen = gen_randint(rule)
                iters.append(gen)
                continue
            except ValueError:
                pass


        iters.append(gen_empty())
    
    return iters

def gen_empty(rule:str):
    while True:
        yield ''

def gen_randint(rule: str):
    '''
    根据规则生成随机数迭代器
    A-B => 生成A-B范围的随机数，支持规则简略
    B   => 相当于 0-B
    A-  => 相当于 A-2^31-1
    '''
    # 分析规则，获取 a 和 b
    if '-' in rule:
        parts = rule.split('-')
        if parts[0] == '':  # 规则是 "-B"
            a = 0
            b = int(parts[1])
        elif parts[1] == '':  # 规则是 "A-"
            a = int(parts[0])
            b = MAXINT  # 使用最大整数作为上限
        else:  # 规则是 "A-B"
            a = int(parts[0])
            b = int(parts[1])
    else:  # 规则是 "B"
        a = 0
        b = int(rule)
    
    # 无限生成随机数
    while True:
        yield random.randint(a, b)