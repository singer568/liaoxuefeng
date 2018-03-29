# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#列表生成式


def triangles1():
    b = [1]
    while True:
        yield b
        b.append(0)
        b = [b[i-1] + b[i] for i in range(len(b))]


def triangles2():
    ret = [1]
    while True:
        yield ret
        for i in range(1,len(ret)):
            ret[i] = pre[i] + pre[i-1]
        ret.append(1)
        pre = ret[:]


def yanghui(num=10):
    aa = [[1]]
    for i in range(1, num):
        aa.append([(0 if j == 0 else aa[i-1][j-1]) + (0 if j == len(aa[i-1]) else aa[i-1][j]) for j in range(i+1)])
    return aa

