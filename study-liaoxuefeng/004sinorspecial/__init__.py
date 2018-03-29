# /usr/bin/evn python3
# -*- coding:utf-8 -*-
from collections import Iterable
from collections import Iterator
import os
# ---------------------01切片（Slice）  有了切片操作，很多地方循环就不再需要了。Python的切片非常灵活，一行代码就可以实现很多行循环才能完成的操作。

L = ['a', 'b', 'c', 'd', 'e', 'f']
a = [L[0], L[1], L[2]]   # 001 取前3个元素

b = []
for x in range(3):  # 002 取前3个元素
    b.append(L[x])
print(b)

print(L[0:3])    # 003 取前3个元素
print(L[:3])    # 如果下标从0开始，可以不写
print(L[-3:-1])     # 也可以倒着取  记住倒数第一个元素的索引是-1。
print(L[-3:])
print(L[1:4])   # 004 取1到4的元素，不包括第四个

# ---------------------------------------切片的用法
L = list(range(100))   # 创建一个0～99的数列
print(L)

print(L[:10])   # 取前10个数
print(L[-10:])  # 取后10个数
print(L[10:20])     # 取10到20的数
print(L[:10:2])     # 取前10个数，每两个取一个
print(L[::5])       # 所有数，每5个取一个
print(L[:])     # 什么也不写，原样复制一个list

t = (1, 2, 3, 4, 5, 6, 7)  # tuple也可以用切片操作
print(t[:])
print(t[:2])
print(t[2:3])

s = 'abcdefghijklmn'    # 字符串也可以用切片操作
print(s[:])
print(s[1:2])
print(s[:6])


# ---------------------02迭代（Iteration） 当我们使用for循环时，只要作用于一个可迭代对象，for循环就可以正常运行
LL = [1, 2, 3, 4, 5, 6, 7, 8, 9]    # 迭代list tuple
for x in LL:
    print(x)

D = {'a': 1, 'b': 2, 'c': 3}    # 迭代dict key
for k in D.keys():
    print(k)
for v in D.values():    # 迭代dict value
    print(v)
for k, v in D.items():  # 迭代items
    print(k, '---', v)

S = 'abcdefgh'
for s in S:     # 迭代字符串
    print(s)

print(isinstance('abc', Iterable))  # 可迭代的（Iterable） 判断一个对象是否为可迭代的
print(isinstance(['a', 'b', 'c'], Iterable))
print(isinstance((1,2,3), Iterable))
print(isinstance(123, Iterable))
print(isinstance({'a': 1, 'b': 2}, Iterable))

E = [1, 2, 3, 4, 5, 6, 7, 8]
for i, value in enumerate(E):   # 如果想要得到下标，可以用enumerate函数，得到下标
    print(i, '---', value)

for x, y in [(1, 2), (3, 4), (5, 6)]:  # 迭代里面用多个变量，很常见
    print(x, '---', y)


def findminandmax(mm):
    if len(mm) == 0:
        return 0, 0
    if len(mm) == 1:
        return (mm[0], mm[0])
    imax = mm[0]
    imin = mm[0]
    for n in mm:
        if imax < n:
            imax = n
        if imin > n:
            imin = n
    return imin, imax


LLL = [3, 2, 4, 6, 21, 5, 8, 9]
print(findminandmax([]))
print(findminandmax([1]))
print(findminandmax([1, 2]))
print(findminandmax(LLL))

# ---------------------03列表生成式

L = list(range(100))        # 生成list
print(L)
L = list(range(1, 11))
print(L)


L = []                      # 生成每个数的平方
for n in range(100):
    L.append(n * n)
print(L)
L = [x*x for x in range(100)]
print(L)

L = [x*x for x in range(100) if x % 2 == 0]     # 生成偶数的平方
print(L)

L = [m + n for m in 'abc' for n in 'ABC']       # 使用两层循环，可以生成全排列：
print(L)


L = [d for d in os.listdir('.')]        # 列出当前目录下的所有文件和目录名
print(L)

d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}       # for循环其实可以同时使用两个甚至多个变量，比如dict的items()可以同时迭代key和value：
for k, v in d.items():
    print(k, '---', v)

d = {'x': 'A', 'y': 'B', 'z': 'C'}     # 列表生成式也可以使用两个变量来生成list：
t = [k + '=' + v for k, v in d.items()]
print(t)

L = ['Hello', 'World', 'IBM', 'Apple']  # 把一个list中所有的字符串变成小写
t = [s.lower() for s in L]
print(t)

L = ['Hello', 'World', 18, 'Apple', None]  # 把一个list中所有的字符串变成小写, 里面包含数字，None
t = [s.lower() for s in L if isinstance(s, str)]
print(t)

# ---------------------04生成器：generator  一边循环一边计算的机制


L = [x for x in range(100)]
print(L)
L = (x for x in range(4))     # 生成器 把[] 换成()
print(L)
print(next(L))
print('----------')
for n in L:     # 生成器是可迭代的
    print(n)


def fib(imax):      # 斐波拉契数列（Fibonacci），除第一个和第二个数外，任意一个数都可由前两个数相加得到
    n, a, b = 0, 0, 1
    while (n < imax):
        print(b)
        a, b = b, a+b  # 赋值语句，相当于 t = (b, a + b)  t是一个tuple a = t[0] b = t[1]
        n = n + 1       # fib函数实际上是定义了斐波拉契数列的推算规则，可以从第一个元素开始，推算出后续任意的元素，这种逻辑其实非常类似generator。


fib(5)


def fib(imax):      # 如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数，而是一个generator：
    n, a, b = 0, 0, 1
    while (n < imax):
        yield b   # 在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。
        a, b = b, a + b
        n = n + 1
    return 'done'


f = fib(6)
for n in f:     # 我们基本上从来不会用next()来获取下一个返回值，而是直接使用for循环来迭代：
    print(n)


def odd():
    print('step1')
    yield (1)
    print('step2')
    yield (2)
    print('step3')
    yield (3)


o = odd()
next(o)
next(o)
next(o)


g = fib(6)
while True:
    try:
        x = next(g)
        print('g:', x)
    except StopIteration as e:  # 但是用for循环调用generator时，发现拿不到generator的return语句的返回值。如果想要拿到返回值，必须捕获StopIteration错误，返回值包含在StopIteration的value中：
        print('Generator return value:', e.value)
        break;


def trangles(imax):
    h = [1]
    while True:
        yield h
        h = [1] + [h[i-1] + h[i] for i in range(1, len(h))] + [1]


tt = trangles(5)
for i, x in enumerate(tt):
    if i == 10:
        break
    print(x)


# ---------------------05 可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator。可以使用isinstance()判断一个对象是否是Iterator对象：

isinstance((x for x in range(10)), Iterator)   # True    生成器既可以用for调用又可以用next调用，所以即是可迭代的又是迭代器
isinstance((x for x in range(10)), Iterable)   # True

isinstance('abc', Iterable)  # True
isinstance('abc', Iterator)  # False

isinstance({}, Iterable)  # True
isinstance([], Iterable)  # True

isinstance([], Iterator)  # False
isinstance({}, Iterator)  # False
isinstance('abc', Iterator)  # False

# 生成器都是Iterator对象，但list、dict、str虽然是Iterable，却不是Iterator;把list、dict、str等Iterable变成Iterator可以使用iter()函数：
isinstance(iter([]), Iterator)   #True
isinstance(iter({}), Iterator)   #True
isinstance(iter('abc'), Iterator)  #True
'''
你可能会问，为什么list、dict、str等数据类型不是Iterator？

这是因为Python的Iterator对象表示的是一个数据流，Iterator对象可以被next()函数调用并不断返回下一个数据，
直到没有数据时抛出StopIteration错误。可以把这个数据流看做是一个有序序列，但我们却不能提前知道序列的长度，
只能不断通过next()函数实现按需计算下一个数据，所以Iterator的计算是惰性的，只有在需要返回下一个数据时它才会计算。
Iterator甚至可以表示一个无限大的数据流，例如全体自然数。而使用list是永远不可能存储全体自然数的。
'''

for x in [1, 2, 3, 4, 5]:
    print(x)

it = iter([1, 2, 3, 4, 5])   # 两者等价，for可以用迭代器处理
while True:
    try:
        print(next(it))
    except StopIteration as e:
        break
