

from typing import Iterable


def trim_middle(arr:Iterable, n:int):
    a = list(arr)
    if len(a) < n:
        return a, [], 0
    
    l = n // 2
    r = -(l + n % 2)

    return a[0:l], a[r:], len(a) - n


