import random
import time

MAXINT = 2**31 - 1

def interpolation_generator(rules:list[str]):
    '''
Insert number: 
    X-Y   ramdom integer
    X:Y   cycle increment 

    X-  => X-2147483647
    Y   => 0-Y
    X:  => X:2147483647
    :Y  => 0:Y 

Insert timestamp: 
    ts   integer of seconds
    tm   decimal of seconds.millisecond
    ms   integer of millisecond

Insert string:  (TODO)
    sX-Y  ramdom length words and numbers
    wX-Y  ramdom length and words

Insert other: (TODO)
    hN    random N bytes hex value
    uuid  uuid4() 8-4-4-4-12 format string
    A,B,C,...  random enumeration value

    '''
    iters = []
    for rule in rules:

        it = try_time(rule) or try_number(rule) or gen_empty()

        iters.append(it)
    
    return iters


def parse_range(exp:str, sep:str):
    l, r = 0, MAXINT
    if sep in exp:
         _ = exp.split(sep)
         l = _[0] or 0
         r = _[1] or r
    else:
        r = exp or r

    try:
        n, m  = int(l), int(r) 
        return (n, m)
    except ValueError:
        return None


def try_number(rule:str):
    try:
        n = int(rule)
        return gen_randint(0, n)
    except ValueError:
        pass

    if '-' in rule:
        lr = parse_range(rule, '-')
        if lr != None:
            return gen_randint(*lr)
        return None

    if ':' in rule:
        lr = parse_range(rule, ':')
        if lr != None:
            return gen_cycle(*lr)
        return None

    return None
    

def try_time(rule:str):
    if rule in ['ts', 'tm', 'ms']:
        return gen_time(rule)
    return None
    


def gen_empty(rule:str = ''):
    while True:
        yield ''

def gen_randint(n, m):
    while True:
        yield random.randint(n, m)

def gen_cycle(l, r):
    n = l
    while True:
        yield n

        if n == r:
            n = l
        n += 1

def gen_time(fmt):
    f = lambda x:x
    
    if fmt == 'ts':
        f = lambda x:int(x)
    if fmt == 'ms':
        f = lambda x:int(x*1000)
    
    while True:
        yield f(time.time())
