#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" OOP的高级特性"""
__author__ = 'wuershan'
'''------------------------------------------------------------------part1 __slot__'''
import socketserver
from enum import Enum, unique
#Python允许在定义class的时候，定义一个特殊的__slots__变量，来限制该class实例能添加的属性
class Student(object):
    __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称

s = Student()
s.name = 'wuershan'
s.age = 18
#s.score = 98 报错

#__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用的
class GraduateStudent(Student):
    pass
g = GraduateStudent()
g.score = ''  # 子类不受限制

'''------------------------------------------------------------------part2 @property '''
# 把get，set方法变为属性调用，装饰器（decorator）可以给函数动态加上功能，对于类的方法，装饰器一样起作用。Python内置的@property装饰器就是负责把一个方法变成属性调用的：

class Student1(object):
    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('value must be int')
        if value < 0 or value > 100:
            raise ValueError('value must 0 ~100')
        self._score = value
#把一个getter方法变成属性，只需要加上@property就可以了，此时，@property本身又创建了另一个装饰器@score.setter，负责把一个setter方法变成属性赋值，于是，我们就拥有一个可控的属性操作
s = Student1()
s.score = 99
print(s.score)

class Student(object):
    @property
    def birth(self):
        return self._birth
    @birth.setter
    def birth(self, value):
        self._birth = value
    @property
    def age(self):   # 只读属性，没定义setter方法
        return 2015-self._birth

'''------------------------------------------------------------------part3 多重继承'''
# 通常都是单一继承，如果想混入其他功能，可以通过多重继承实现MixIn
#MixIn的目的就是给一个类增加多个功能，这样，在设计类的时候，我们优先考虑通过多重继承来组合多个MixIn的功能，而不是设计多层次的复杂的继承关系。
# 编写一个多进程模式的TCP服务，定义如下
class MyTcpServer(socketserver.TCPServer,socketserver.ForkingMixIn):
    pass
# 编写一个多线程模式的UDP服务，定义如下：
class MyUDPServer(socketserver.UDPServer, socketserver.ThreadingMixIn):
    pass
# 如果你打算搞一个更先进的协程模型，可以编写一个CoroutineMixIn：
#class MyTCPServer(socketserver.TCPServer, socketserver.CoroutineMixIn):
# 这样一来，我们不需要复杂而庞大的继承链，只要选择组合不同的类的功能，就可以快速构造出所需的子类。
'''------------------------------------------------------------------part4 定制类'''
# 1、__str__ __repr__() 类似java的toString
class Student(object):
    def __init__(self, name):
        self._name = name
    def __str__(self): # 返回用户看到的字符串
        return 'Student name is %s'%self._name
    __repr__ = __str__   # 开发人员调试用

s = Student('dddd')
print(s)

#2、__iter__ 用于对象的迭代，用于 for ... in循环，该方法返回一个迭代对象，Python的for循环就会不断调用该迭代对象的__next__()方法拿到循环的下一个值，直到遇到StopIteration错误时退出循环。
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b

    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 100000: # 退出循环的条件
            raise StopIteration()
        return self.a # 返回下一个值

for n in Fib():
     print(n)
# 3、使Fib能像list一样通过，Fib[5]得到某个具体数据，需要实现__getitem__方法
class Fib(object):
    def __getitem__(self, n):# n可能是个整数，也可能是个切片
        if isinstance(n, int): # n是整数
            a, b = 1, 1
            for x in range(n):
                a, b = b, a+b
            return a
        if isinstance(n, slice): # n是切片
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L
f = Fib()
f[0]
f[1]

f[0:5] #没有对step做处理，没有对负数处理，

# 4、__getattr__() 动态返回一个属性，只有在没有找到属性的情况下，才调用__getattr__
class Student(object):

    def __init__(self):
        self.name = 'Michael'

    def __getattr__(self, attr):   #如果调用score属性，就可以这样用
        if attr=='score':
            return 99
        raise AttributeError('\'Student\' object has no attribute \'%s\'' % attr)

s = Student()
s.name
s.score #返回99

class Chain(object):

    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__
g= Chain().status.user.timeline.list
print(g) #/status/user/timeline/list
#这样，无论API怎么变，SDK都可以根据URL实现完全动态的调用，而且，不随API的增加而改变！
#还有些REST API会把参数放到URL中，比如GitHub的API：GET /users/:user/repos
#调用时，需要把:user替换为实际用户名。如果我们能写出这样的链式调用：Chain().users('michael').repos就可以非常方便地调用API了。

# 5、__call__ 任何类，只需要定义一个__call__()方法，就可以直接对实例进行调用。请看示例：
class Student(object):
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print('My name is %s.' % self.name)
s = Student('Michael')
print(s())

#那么，怎么判断一个变量是对象还是函数呢？其实，更多的时候，我们需要判断一个对象是否能被调用，能被调用的对象就是一个Callable对象，
# 比如函数和我们上面定义的带有__call__()的类实例：
callable(Student())  #True
callable(max) #True
callable([1, 2, 3]) #False

# 6、枚举类型定义一个class类型，然后，每个常量都是class的一个唯一实例。Python提供了Enum类来实现这个功能：
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)
#value属性则是自动赋给成员的int常量，默认从1开始计数。
#如果需要更精确地控制枚举类型，可以从Enum派生出自定义类：
@unique #@unique装饰器可以帮助我们检查保证没有重复值。
class Weekday(Enum):
    Sun = 0 # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
day1 = Weekday.Mon
print(Weekday.Tue)
print(Weekday['Tue'])
print(Weekday.Tue.value)
print(day1 == Weekday.Mon)
print(day1 == Weekday.Tue)
print(Weekday(1))
print(day1 == Weekday(1))
Weekday(7)

#既可以用成员名称引用枚举常量，又可以直接根据value的值获得枚举常量。


#使用type()动态创建类，动态语言本身支持运行期动态创建类，这和静态语言有非常大的不同，要在静态语言运行期创建类，必须构造源代码字符串再调用编译器，或者借助一些工具生成字节码实现，本质上都是动态编译，会非常复杂。
#先定义metaclass，就可以创建类，最后创建实例。












