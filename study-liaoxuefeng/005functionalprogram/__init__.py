# /usr/bin/evn python3
# -*- coding:utf-8 -*-
from functools import reduce
import functools
import time
# ------------------------------------高阶函数--------begin
f = abs   # 函数名其实就是指向函数的变量！对于abs()这个函数，完全可以把函数名abs看成变量，它指向一个可以计算绝对值的函数！
print(f(-5))

# abs=10
# print(abs)  # 输出10
'''
由于abs函数实际上是定义在import builtins模块中的，所以要让修改abs变量的指向在其它模块也生效，
要用import builtins; builtins.abs = 10
'''

'''
既然变量可以指向函数，函数的参数能接收变量，那么一个函数就可以接收另一个函数作为参数，这种函数就称之为高阶函数
编写高阶函数，就是让函数的参数能够接收别的函数
'''
def add(x, y, f):
    return f(x) + f(y)
print(add(-5, 6, abs))
# ------------------------------------高阶函数--------end
# ------------------------------------高阶函数举例（map/reduce;filter;sorted）--------begin
'''
map()函数接收两个参数，一个是函数，一个是Iterable，
map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回。
函数f(x)=x2，作用在一个list [1, 2, 3, 4, 5, 6, 7, 8, 9]上
'''
def f(x):
    return x*x
L = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(list(map(f, L)))  # 把map返回的iterator转换成list输出
print(list(map(str, L)))
'''
再看reduce的用法。reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，
reduce把结果继续和序列的下一个元素做累积计算，其效果就是：reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
'''
def f(x, y):
    return x + y
print(reduce(f, L))

def f(x, y):
    return x * 10 + y
print(reduce(f, [1, 3, 5, 7, 9]))    # 如果要把序列[1, 3, 5, 7, 9]变换成整数13579，reduce就可以派上用场

def char2num(s):
    digits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    return digits[s]
print(reduce(f, map(char2num, '13579')))  # 如果考虑到字符串str也是一个序列，对上面的例子稍加改动，配合map()，我们就可以写出把str转换为int的函数：

DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
def str2int(s):     # 整理成一个str2int的函数就是：
    def fn(x, y):
        return x * 10 + y
    def char2num(s):
        return DIGITS[s]
    return reduce(fn, map(char2num, s))

def char2num(s):
    return DIGITS[s]
def str2int(s):
    return reduce(lambda x, y : x * 10 + y, map(char2num, s))


def normalize(s):   # 输出 ['Adf', 'Gdf', 'Few']
    return s[0].upper() + s[1:].lower()
m = map(normalize, ['adf', 'gdf','few'])
print(list(m))

def prod(L):
    def fn(x, y):
        return x * y
    return reduce(fn, L)
print(prod([1, 2, 3, 4, 5, 6]))

def str2float(s):
    ix = s.split('.')
    t = len(ix[1])
    s = s.replace('.','')
    def char2num(a):
        DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
        return DIGITS[a]
    def toint(x, y):
        return x * 10 + y

    rs = reduce(toint, map(char2num, s))
    return  rs/pow(10, t)

print(str2float('1.456'))


'''
filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素。
注意到filter()函数返回的是一个Iterator，也就是一个惰性序列，所以要强迫filter()完成计算结果，需要用list()函数获得所有结果并返回list。
'''
def is_odd(s):
    return s % 2 == 1
print(list(filter(is_odd, [1,2,3,4,5,6])))

def not_empty(s):
    return s and s.strip()
print(list(filter(not_empty, ['1', '', '  ', '2'])))


def _not_divisible(n):
    return lambda x: x % n > 0
def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n

def primes():
    yield 2
    it = _odd_iter() # 初始序列
    while True:
        n = next(it) # 返回序列的第一个数
        yield n
        it = filter(_not_divisible(n), it) # 构造新序列

# 打印1000以内的素数:
for n in primes():
    if n < 1000:
        print(n)
    else:
        break


# 回数是指从左向右读和从右向左读都是一样的数，例如12321，909。请利用filter()筛选出回数：
def isReverse(s):
    return str(s) == str(s)[::-1]
'''
 切片操作中list = [s:e:L],s代表开始索引值，e表示结束索引值的前一位，L表示步进值,
 当步进值为负数时，s默认置为-1，e默认置为-len(list)-1,所以[::-1] ==[-1:-len(list)-1:-1]
 即按照步进值为1，从最后一位到第一位完整复制一遍
'''

print(list(filter(isReverse, range(1,100))))

'''
sorted(序列，key)按照key指定的要求排序
'''
print(sorted([0,7,3,2,4,6,9], key=abs))

sorted(['bob', 'about', 'Zoo', 'Credit'])  # 按照ascii码排序
sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower)  # 按照小写字母排序
sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)   # 进行反向排序

'''
假设我们用一组tuple表示学生名字和成绩：
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
请用sorted()对上述列表分别按名字排序：
'''
def by_name(t):
    return t[0].lower()
def by_score(t):
    return -t[1]
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
L2 = sorted(L, key = by_name)
L3 = sorted(L, key=by_score,reverse=True)
print(L2)
print(L3)

# ------------------------------------高阶函数举例（map/reduce;filter;sorted）--------end
# ------------------------------------返回函数，闭包--------begin
'''
返回函数，闭包  当我们调用lazy_sum()时，每次调用都会返回一个新的函数，即使传入相同的参数
返回闭包时牢记一点：返回函数不要引用任何循环变量，或者后续会发生变化的变量。 
'''
def lazy_sum(*args):
    def sum1():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum1
f = lazy_sum(1, 3, 5, 7, 9)
print(f())

def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs

f1, f2, f3  = count()
print(f1())  # 你可能认为调用f1()，f2()和f3()结果应该是1，4，9，但实际结果全是9；原因就在于返回的函数引用了变量i，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量i已经变成了3，因此最终结果为9。
print(f2())
print(f3())


def count():
    def f(j):
        def g():
            return j*j
        return g
    fs = []
    for i in range(1, 4):
        fs.append(f(i)) # f(i)立刻被执行，因此i的当前值被传入f()
    return fs


def createCounter(*args):
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

counterA = createCounter()
print(counterA())
print(counterA())

'''
1.内部函数一般无法修改外部函数的参数 
2.想要修改需要声明 nonlocal 
3.内部函数可以修改外部list中的元素   而内部函数的str型变量做不到（所以要声明 Nonelocal）
'''
def createCounter():
    s = [0]
    def counter():
        s[0] = s[0] + 1
        return s
    return counter
c = createCounter()
print(c())
print(c())

# ------------------------------------返回函数，闭包--------end
# ------------------------------------匿名函数,lambda--------begin
'''
关键字lambda表示匿名函数，冒号前面的x表示函数参数。
匿名函数有个限制，就是只能有一个表达式，不用写return，返回值就是该表达式的结果。
'''
f = lambda x : x*x
print(f(2))

L = list(filter(lambda x: x % 2 == 1, range(1, 20)))
print(L)
# ------------------------------------匿名函数,lambda--------end
# ------------------------------------装饰器---函数运行期间动态增加功能的方式-叫装饰器，decorator就是一个返回函数的高阶函数----begin
def now():
    print('2018-03-26')
print(now.__name__)   # 表示函数名称

#定义一个打印日志的decorator
def log(func):
    def wrapper(*args, **kw):
        print('call %s():'% func.__name__)
        return func(*args, **kw)
    return wrapper

@log                      # 等同于 now = log(now)
def now():
    print('2018-03-26')
now()

#如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数，写出来会更复杂。比如，要自定义log的文本：
def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():'%(text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@log('execute') # 等同于 now = log('execute')(now)  ,首先执行log('execute')，返回的是decorator函数，再调用返回的函数，参数是now函数，返回值最终是wrapper函数。
def now():
    print('2018-03-26')
now()
print(now.__name__)
# 函数也是对象，它有__name__等属性，但你去看经过decorator装饰之后的函数，它们的__name__已经从原来的'now'变成了'wrapper'：

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('call %s():'%func.__name__)
        return func(*args, **kw)
    return wrapper
# 或者
def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s%s():'%(text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

def metric(func):  #打印执行时间
    @functools.wraps(func)
    def wrapper(*args, **kw):
        s_time = time.time()
        fn = func(*args, **kw)
        e_time = time.time() - s_time
        print('%s executed in %s ms'%(func.__name__, e_time))
        return fn
    return wrapper

@metric
def fast(x, y):
    time.sleep(0.0012)
    return x+y
f = fast(11, 22)
# ------------------------------------装饰器---函数运行期间动态增加功能的方式-叫装饰器，decorator就是一个返回函数的高阶函数----end
# ------------------------------------偏函数----begin
# int()函数是将字符串转换为整数，默认按10进制转换，如果指定base可以做任何进制转换，定义个int2做大量的2进制转换
def int2(s, base=2):
    return int(s, base)
# functools.partial 可以帮助我们创建一个偏函数，不需要我们自己定义int2
int2 = functools.partial(int, base=2)
print(int2('1000')) # 把二进制转为10进制

# functools.partial的作用就是，把一个函数的参数给固定住（也就是默认值），返回一个新的函数，调用这个函数会更简单，
# 即偏函数仅仅固定了默认值，后面如果想改变也可以更改
print(int2('1000000', base=10))
#创建偏函数时，实际上可以接收函数对象，*args，**kw这3个参数，当传入：
int2 = functools.partial(int, base=2) #实际上固定了int()函数的关键字参数base，也就是：
int2('10010') # 相当于
kw = { 'base': 2 }
int('10010', **kw)
#当传入：
max2 = functools.partial(max, 10)
#实际上会把10作为*args的一部分自动加到左边，也就是：
max2(5, 6, 7)
#相当于：
args = (10, 5, 6, 7)
max(*args)
# ------------------------------------偏函数----end
