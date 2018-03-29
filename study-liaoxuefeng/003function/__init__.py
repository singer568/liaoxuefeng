# 第三章 函数
# -*- coding:utf-8 -*-
import math   # 需要放在文件第一行

# --    01调用函数  --
print(abs(-1))
print(max(1, 2, 3))
n1 = 255
n2 = 1000
print(hex(255))
print(hex(1000))

# --    02定义函数  --


def myabs(n):
    if n > 0:
        return n
    else:
        return -n


print(myabs(9))
print(myabs(-9))
print('''
如果你已经把my_abs()的函数定义保存为abstest.py文件了，
那么，可以在该文件的当前目录下启动Python解释器，
用from abstest import my_abs来导入my_abs()函数，
注意abstest是文件名（不含.py扩展名）
from abstest import myabs
myabs(-9)
''')


def nop():  # 空函数,pass也可以用在if语句中，如果...直接pass，占位符，先跑通代码再说，
    pass


def myabs(n):   # 与abs函数的区别是,abs有类型检查，而myabs没有，需要改造
    if not isinstance(n, (int, float)):
        raise TypeError('bad operand type')
    if n > 0:
        return n
    else:
        return -n


def move(x, y, step, angle=0):  # 函数返回多个值
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny


x, y = move(100, 100, 60, math.pi / 6)
print(x, y)    # 但其实这只是一种假象，Python函数返回的仍然是单一值：

r = move(100, 100, 60, math.pi / 6)
print(r)  #  原来返回的是一个tuple


def quadratic(a, b, c):
    a = int(a)
    b = int(b)
    c = int(c)
    t = b*b - 4*a*c
    if t < 0:
        print('方程式无解')
    elif t == 0:
        x = -b/(2*a);
        return x, x
    else:
        x1 = (math.sqrt(t)-b)/(2*a)
        x2 = (-math.sqrt(t)-b)/(2*a)
        return x2, x2


print(quadratic(2, 3, 1))

# --    03函数的参数 --


def power(k, n=2):  # 计算k的n次方, 函数增加默认值，一是必选参数在前，默认参数在后；把变化大的参数放前面，变化小的参数放后面，变化小的参数就可以作为默认参数
    s = 1   # 定义默认参数要牢记一点：默认参数必须指向不变对象！ 不能用list
    while n > 0:
        n = n - 1
        s = s*k
    return s


print(power(5))
print(power(5, 3))


def add_end(a=[]):    # 可变变量，一定不能用list或者dictionry
    a.append('END')
    print(a)
    return a


print('''
Python函数在定义的时候，默认参数a的值就被计算出来了，即[]，因为默认参数a也是一个变量，
它指向对象[]，每次调用该函数，如果改变了a的内容，则下次调用时，默认参数的内容就变了，
不再是函数定义时的[]了。
''')

add_end()
add_end()   # 输出两个END


def addend(a=None):
    if a is None:
        a = []
    a.append('END')
    print(a)
    return a


addend()
addend()


def calc(numbers):  # 参数个数不确定
    s = 0
    for t in numbers:
        s = s + t
    print(s)
    return s


calc([1, 2, 3, 4, 5, 6])
calc((1, 2, 3, 4))


def calcs(*numbers):  # 变成可变参数，调用起来简单
    s = 0
    for t in numbers:
        s = s + t
    print(s)
    return s


calcs(1, 2, 3, 4, 5)   # 可变参数时，可简化调用
calcs(1, 2, 3)
# calcs([1, 2, 3, 4, 5, 6]) 这时候调用会报错，参数错误
# calcs((1, 2, 3, 4))

p = [1, 2, 3, 4, 5, 6]
q = (1, 2, 3, 4)
calcs(*p)   # 将元组变为可变参数
calcs(*q)   # 将元组变为可变参数


def person(name, age, **kw):  # 关键字参数 关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict
    print('name:', name, 'age:', age, 'other:', kw)


person('kewu', 30)
person('kewu', 30, city='beijing', male='M')

print('''
关键字参数有什么用？它可以扩展函数的功能。比如，在person函数里，我们保证能接收到name和age这两个参数，
但是，如果调用者愿意提供更多的参数，我们也能收到。试想你正在做一个用户注册的功能，除了用户名和年龄是必填项外，
其他都是可选项，利用关键字参数来定义这个函数就能满足注册的需求。
''')
extra = {'city': 'beijing', 'male': 'M'}
person('kewu', 30, **extra)


def person(name, age, **kw):  # 检查city，male是否在关键字参数里面
    if 'city' in kw:
        print('有city参数')
    if 'male' in kw:
        print('有male参数')
    print('name:', name, 'age:', age, 'other:', kw)


person('kewu', 30, city='beijing', male='M', good='yes')


def person(name, age, *, city, job):  # 命名关键字参数 如果要限制关键字参数的名字，就可以用命名关键字参数，例如，只接收city和job作为关键字参数。
    print(name, age, city, job)  # 和关键字参数**kw不同，命名关键字参数需要一个特殊分隔符*，*后面的参数被视为命名关键字参数。


person('jack', 30, city='beijing', job='engineer')


def person(name, age, *args, city, job):  # 如果函数定义中已经有了一个可变参数，后面跟着的命名关键字参数就不再需要一个特殊分隔符*了：
    print(name, age, args, city, job)


# person('Jack', 24, 'Beijing', 'Engineer')  # 命名关键字参数必须传入参数名，这和位置参数不同。如果没有传入参数名，调用将报错
def person(name, age, *, city='Beijing', job):  # city可以有默认值
    print(name, age, city, job)


person('jack', 30, job='engineer')

#位置参数
def person(name, age, city, job):  # 使用命名关键字参数时，要特别注意，如果没有可变参数，就必须加一个*作为特殊分隔符。如果缺少*，Python解释器将无法识别位置参数和命名关键字参数：
    # 缺少 *，city和job被视为位置参数
    pass


#参数组合
'''
在Python中定义函数，可以用必选参数、默认参数、可变参数、关键字参数和命名关键字参数，
这5种参数都可以组合使用。但是请注意，参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数。
'''


def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)


def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)


f1(1, 2)
f1(1, 2, c=3)
f1(1, 2, 3, 'a', 'b')
f1(1, 2, 3, 'a', 'b', x=99)
f2(1, 2, d=99, ext=None)

args = (1, 2, 3, 4)   # 最神奇的是通过一个tuple和dict，你也可以调用上述函数：所以，对于任意函数，都可以通过类似func(*args, **kw)的形式调用它，无论它的参数是如何定义的。
kw = {'d': 99, 'x': '#'}
f1(*args, **kw)
args = (1, 2, 3)
kw = {'d': 88, 'x': '#'}
f2(*args, **kw)   #  虽然可以组合多达5种参数，但不要同时使用太多的组合，否则函数接口的可理解性很差。


# 递归函数

def fn(n): # 阶乘n! = 1 x 2 x 3 x ... x n
    if n == 1:
        return 1
    else:
        return n*fn(n-1)

print(fn(10))

'''
使用递归函数需要注意防止栈溢出。在计算机中，函数调用是通过栈（stack）这种数据结构实现的，每当进入一个函数调用，栈就会加一层栈帧，
每当函数返回，栈就会减一层栈帧。由于栈的大小不是无限的，所以，递归调用的次数过多，会导致栈溢出。
解决递归调用栈溢出的方法是通过尾递归优化，事实上尾递归和循环的效果是一样的，所以，把循环看成是一种特殊的尾递归函数也是可以的。

尾递归是指，在函数返回的时候，调用自身本身，并且，return语句不能包含表达式
这样，编译器或者解释器就可以把尾递归做优化，使递归本身无论调用多少次，都只占用一个栈帧，不会出现栈溢出的情况。
上面的fact(n)函数由于return n * fact(n - 1)引入了乘法表达式，所以就不是尾递归了。
要改成尾递归方式，需要多一点代码，主要是要把每一步的乘积传入到递归函数中：

'''


def fact(n):
    return fact_iter(n, 1)


def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)

'''
尾递归调用时，如果做了优化，栈不会增长，因此，无论多少次调用也不会导致栈溢出。
遗憾的是，大多数编程语言没有针对尾递归做优化，Python解释器也没有做优化，所以，
即使把上面的fact(n)函数改成尾递归方式，也会导致栈溢出。
'''