# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""使用异步IO来编写程序性能会远远高于同步IO，但是异步IO的缺点是编程模型复杂。想想看，你得知道什么时候通知你“汉堡做好了”，
而通知你的方法也各不相同。如果是服务员跑过来找到你，这是回调模式，如果服务员发短信通知你，你就得不停地检查手机，这是轮询模式。
总之，异步IO的复杂度远远高于同步IO。"""

__author__='wuershan'

from io import StringIO
from io import BytesIO
import  os
import pickle
import json

''' ----------------------------------------------------------------------------------------------------- part1 文件读写'''
f = open('/home/wes/soft/pycharm/test/b.txt', 'r')
g = f.read()
print(g)
f.close()

try:    # try finally 保证每次用完了都能把文件关闭
    f = open('/home/wes/soft/pycharm/test/b.txt', 'r')
    print(f.read())
finally:
    if f:
        f.close()

with open('/home/wes/soft/pycharm/test/b.txt', 'r') as f:   #用with相等与try finally
    print(f.read())

# 调用read()会一次性读取文件的全部内容，如果文件有10G，内存就爆了，所以，要保险起见，可以反复调用read(size)方法，
# 每次最多读取size个字节的内容。另外，调用readline()可以每次读取一行内容，调用readlines()一次读取所有内容并按行返回list。
# 因此，要根据需要决定怎么调用。
# 如果文件很小，read()一次性读取最方便；如果不能确定文件大小，反复调用read(size)比较保险；如果是配置文件，调用readlines()最方便：
with open('/home/wes/soft/pycharm/test/b.txt', 'r') as f:   #用with相等与try finally
    for line in f.readlines():
        print(line.strip())

####file-like Object 像open()函数返回的这种有个read()方法的对象，在Python中统称为file-like Object。
# 除了file外，还可以是内存的字节流，网络流，自定义流等等。
# file-like Object不要求从特定类继承，只要写个read()方法就行。StringIO就是在内存中创建的file-like Object，常用作临时缓冲。

#读取二进制文件
#f = open('/Users/michael/test.jpg', 'rb')
#要读取非UTF-8编码的文本文件，需要给open()函数传入encoding参数，例如，读取GBK编码的文件：
#f = open('/Users/michael/gbk.txt', 'r', encoding='gbk', errors='ignore')

#写文件
with open('/home/wes/soft/pycharm/test/a.txt', 'w') as f: # 如果文件不存在，则新建文件，如果文件存在则覆盖掉原文件
    f.write('again hello world')

with open('/home/wes/soft/pycharm/test/b.txt', 'a') as f: # a表示以追加的方式写入
    f.write('again hello world')

''' ----------------------------------------------------------------------------------- part2 StringIO和BytesIO'''

#StringIO 内存中读写str
f = StringIO()
f.write('hello')   # 写内存数据
f.write(' ')
f.write('world!')
print(f.getvalue())

f = StringIO('Hello \n Wrold \n Goodbye')  # 读内存数据
while True:
    s = f.readline()
    if s=='' :
        break;
    print(s.strip())

# StringIO操作的只能是str，如果要操作二进制数据，就需要使用BytesIO。
f = BytesIO()
f.write('中文'.encode('utf-8')) # 写二进制
print(f.getvalue())

#请注意，写入的不是str，而是经过UTF-8编码的bytes。和StringIO类似，可以用一个bytes初始化BytesIO，然后，像读文件一样读取：
f = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
print(f.read())

''' ----------------------------------------------------------------------------------- part3 操作文件和目录'''
print(os.name)
print(os.uname())
print(os.environ) #环境变量
print(os.environ.get('PATH')) #获取某个环境变量的值


# 操作文件和目录，操作文件和目录的函数一部分放在os模块中，一部分放在os.path模块中
g = os.path.abspath('.') # 查看当前目录的绝对路径:
print(g)
#把两个路径合成一个时，不要直接拼字符串，而要通过os.path.join()函数，这样可以正确处理不同操作系统的路径分隔符/和\的问题
os.path.join('/home/wes/soft/pycharm/test', 'testdir') # 在某个目录下创建一个新目录，首先把新目录的完整路径表示出来
os.mkdir('/home/wes/soft/pycharm/test/testdir') # # 然后创建一个目录
os.rmdir('/home/wes/soft/pycharm/test/testdir')  # 删除一个目录
g = os.path.split('/home/wes/soft/pycharm/test/g') # 要拆分路径时，也不要直接去拆字符串，而要通过os.path.split()函数
print(g)

#os.path.splitext()可以直接让你得到文件扩展名
g = os.path.splitext('/home/wes/soft/pycharm/test/a.txt')  # 这些合并、拆分路径的函数并不要求目录和文件要真实存在，它们只对字符串进行操作。
print(g)
#os.rename('a.txt', 'b.txt')
#os.remove('b.txt')

#幸运的是shutil模块提供了copyfile()的函数，你还可以在shutil模块中找到很多实用函数，它们可以看做是os模块的补充。
#列出当前目录下的所有目录，只需要一行代码：
g = [x for x in os.listdir('.') if os.path.isdir(x)]
print(g)
# 要列出所有的.py文件，也只需一行代码
[x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']
#编写一个程序，能在当前目录以及当前目录的所有子目录下查找文件名包含指定字符串的文件，并打印出相对路径。
def showAllFiles(path):
    files = [x for x in os.listdir(path)]
    p = path
    for item in files:
        if os.path.isdir(os.path.join(p,item)):
            showAllFiles(os.path.join(path,item))
        else:
            print(os.path.join(p, item))

showAllFiles('/home/wes/soft/pycharm/test')

''' ----------------------------------------------------------------------------------- part4 序列化 pickle模块来实现序列化'''
d = dict(name='Bob', age=20, score=88)
g = pickle.dumps(d)  # pickle.dumps()方法把任意对象序列化成一个bytes ,就可以把这个bytes写入文件。或者用另一个方法pickle.dump()直接把对象序列化后写入一个file-like Object：
print(g)

f = open('/home/wes/soft/pycharm/test/dump.txt', 'wb')   #序列化到文件
pickle.dump(d, f)
f.close()

f = open('/home/wes/soft/pycharm/test/dump.txt', 'rb') # 从文件反序列化
d = pickle.load(f)
print(d)  # 这个变量和原来的变量是完全不相干的对象，它们只是内容相同而已。
f.close()

#序列化为json
d = dict(name='中文', age=20, score=88)
json.dumps(d)  #dump()方法可以直接把JSON写入一个file-like Object。
#要把JSON反序列化为Python对象，用loads()或者对应的load()方法，前者把JSON的字符串反序列化，后者从file-like Object中读取字符串并反序列化：
json_str = '{"age": 20, "score": 88, "name": "Bob"}'
json.loads(json_str)

# 对象的序列化
class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

s = Student('Bob', 20, 88)

def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }
print(json.dumps(s, default=student2dict))  # 类不知道如何序列化为json，需要建立映射关系
print(json.dumps(s, default=lambda obj: obj.__dict__)) # 利用类的__dict__属性，它就是一个dict，用来存储实例变量


def dict2student(d):  # 反序列化，建立一个映射关系
    return Student(d['name'], d['age'], d['score'])


d = dict(name='中文吴二山', age=20, score=88)
print(json.dumps(d, ensure_ascii=False))