#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" object oriented programming  part1  class and instance """

__author__='wuershan'

import types

class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self):
        print('%s : %s'%(self.name, self.score))

    def get_grade(self):
        if self.score >= 90:
            return 'A'
        elif self.score >= 60:
            return 'B'
        else:
            return 'C'



stu = Student('wuershan', 89)
stu2 = Student('lifeng', 98)
stu.print_score()
stu2.print_score()

g = stu.get_grade()
g1 = stu2.get_grade()
print(g)
print(g1)

""" object oriented programming  part2  vist restrict 访问限制 """

class Student1(object):
    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s : %s'%(self.__name, self.__score))

    def get_score(self):
        return self.__score
    def get_name(self):
        return self.__name
    def set_score(self, score):
        if 0 <= score <= 100:
            self.__score = score
        else:
            raise ValueError('Bad Score')

s1 = Student1('wuershan', 98)
s1.__name = '3333'  # 不能这样用
print(s1.__name)   # 虽然也可以改变，但不能这样使用，表面上看，外部代码“成功”地设置了__name变量，但实际上这个__name变量和class内部的__name变量不是一个变量！内部的__name变量已经被Python解释器自动改成了_Student__name，而外部代码给bart新增了一个__name变量。不信试试：
print(s1.get_name())
#以双下划线开头，并且以双下划线结尾的，__xx__,是特殊变量，特殊变量是可以直接访问的，不是private变量
#private 是__XX是私有变量,不能用__name__、__score__这样的变量名
#你会看到以一个下划线开头的实例变量名，比如_name，这样的实例变量外部是可以访问的，
# 但是，按照约定俗成的规定，当你看到这样的变量时，意思就是，“虽然我可以被访问，但是，请把我视为私有变量，不要随意访问”
#双下划线开头的实例变量是不是一定不能从外部访问呢？其实也不是。不能直接访问__name是因为Python解释器对外把__name变量改成了_Student__name，
# 所以，仍然可以通过_Student__name来访问__name变量： bart._Student__name,但是强烈建议你不要这么干，
# 因为不同版本的Python解释器可能会把__name改成不同的变量名。

""" object oriented programming  part3 extend and plomorphic 继承和多态 """
class Animal(object):
    def __init__(self, name):
        self.__name = name

    def run(self):
        print('This is Animal Run')

class Dog(Animal):
    def run(self):
        print('This is Dog Run')
class Cat(Animal):
    def run(self):
        print('This is Cat Run')

d = Dog('Dog')
d.run()

def run_twice(animal):
    animal.run()
    animal.run()
run_twice(d)
#对于静态语言（例如Java）来说，如果需要传入Animal类型，则传入的对象必须是Animal类型或者它的子类，否则，将无法调用run()方法。
#对于Python这样的动态语言来说，则不一定需要传入Animal类型。我们只需要保证传入的对象有一个run()方法就可以了：
class Timer(object):
    def run(self):
        print('Start...')
#这就是动态语言的“鸭子类型”，它并不要求严格的继承体系，一个对象只要“看起来像鸭子，走起路来像鸭子”，那它就可以被看做是鸭子。
#Python的“file-like object“就是一种鸭子类型。对真正的文件对象，它有一个read()方法，返回其内容。但是，许多对象，只
# 要有read()方法，都被视为“file-like object“。许多函数接收的参数就是“file-like object“，你不一定要传入真正的文件对象，
# 完全可以传入任何实现了read()方法的对象。


""" object oriented programming  part4: Get Object's Information 获取对象信息 """
# 用type判断对象类型
print(type(123))
print(type(abs))
print(type(d))
type('abc') == str
type(123) == int

def fn():
    pass
type(fn) == types.FunctionType
type(abs) == types.BuiltinFunctionType
type(lambda x : x*x) == types.LambdaType
type(x for x in range(1,5)) == types.GeneratorType
# 用isinstance判断对象类型
isinstance(d, Dog)
isinstance('a', str)
isinstance(123, int)
isinstance(b'a', bytes)
# 用dir()
print(dir('ABC'))
len('ABC') # 实际上调用的是字符串里面的__len__方法
'ABC'.__len__()
# 我们自己写的类，如果也想用len(myObj)的话，就自己写一个__len__()方法：
class MyDog(Animal):
    def __len__(self):
        return 100
mydog = MyDog('dog')
print(len(mydog))

#仅仅把属性和方法列出来是不够的，配合getattr()、setattr()以及hasattr()，我们可以直接操作一个对象的状态：
#hasattr(mydog, 'x')
#getattr(mydog, 'x')
#getattr(mydog, 'x', 404) # 传入默认值，如果属性不存在，返回404
#setattr(mydog, 'x', 19)

""" object oriented programming  part5: instance attribute and class attribute 实例属性和类属性 """
class Student2(object):
    name = 'student'
    pass

s = Student2()
print(s.name)
print(Student2.name)
s.name = 'jjjj'
Student2.name = 'kkk'
print(s.name)
print(Student2.name)
del s.name
print(s.name)
print(Student2.name)
