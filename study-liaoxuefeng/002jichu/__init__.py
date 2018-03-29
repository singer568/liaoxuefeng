# -*- coding: utf-8 -*-
# python 基础
print(10/3)
print(10//3)
print('this is a string')
print(''' this
is
a 
string
block
''')
print('this is a \\ escape 转义字符')
print(r' r means all this string do not need escape \\')
print('this is boolean variable', 1 > 2)
print('this is boolean variable', 1 <= 2)
print('this is boolean variable', not True)
print('this is boolean variable', 3 and 2)   # 2 and 第一个为真直接取第二个
print('this is boolean variable', 3 or 2)    # 3 or 第一个为真直接取第一个
print('this is boolean variable', 0 and 2)
print('this is boolean variable', 0 or 2)


# 字符串及编码
print(ord('a'))  # ord()获取字符的整数表示
print(ord('0'))
print(ord('1'))
print(ord('中'))

print(chr(66))  # chr()把编码转成对应字符
print(chr(25991))

print('\u4e2d\u6587')  # 16进制表示，可以直接写

print('''
由于Python的字符串类型是str，在内存中以Unicode表示，
一个字符对应若干个字节。如果要在网络上传输，或者保存到磁盘上，
就需要把str变为以字节为单位的bytes。
''')

print(b'ABC')  # Python对bytes类型的数据用带b前缀的单引号或双引号表示：
print('ABC'.encode('ascii'))  # 以Unicode表示的str通过encode()方法可以编码为指定的bytes
print('中文'.encode('utf-8'))
# print('中文'.encode('ascii'))
print(''' 上面的报错 
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
纯英文的str可以用ASCII编码为bytes，内容是一样的，含有中文的str可以用UTF-8编码为bytes。
含有中文的str无法用ASCII编码，因为中文编码的范围超过了ASCII编码的范围，Python会报错
在bytes中，无法显示为ASCII字符的字节，用\\x##显示。
如果我们从网络或磁盘上读取了字节流，那么读到的数据就是bytes。
要把bytes变为str，就需要用decode()方法：
''')
print(b'ABC'.decode('ascii'))
print(b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8'))

print(b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore'))   # 如果bytes中只有一小部分无效的字节，可以传入errors='ignore'忽略错误的字节：


print(len('ABC'))  # 计算的是字符数
print(len(b'ABC'))   # 计算的是字符占用的字节数
print(len(b'\xe4\xb8\xad\xe6\x96\x87'))
print(len('中'.encode('utf-8')))  # 经过utf-8编码后，一个字符
print('''
1个中文字符经过UTF-8编码后通常会占用3个字节，而1个英文字符只占用1个字节。
''')

# 字符串格式化
# 输出类似 '亲爱的xxx你好！你xx月的话费是xx，余额是xx'
# 采用的格式化方式和C语言是一致的，用%实现
print('''
占位符 	替换内容
%d 	整数
%f 	浮点数
%s 	字符串
%x 	十六进制整数
''')
print('Hello %s' % 'world')
print('Hello %s, your charge is $%d' % ('wuershan', 1000))

print('''
如果你不太确定应该用什么，%s永远起作用，它会把任何数据类型转换为字符串：
''')

print('Hello, {0}, your charge is {1:.1f}'.format('wuershan', 17.321))

print('成绩提升：{0:.1f}%'.format((85-72)/72 * 100))

# list 和 tuple
classmates = ['suyao', 'lifeng', 'yingying']
print(classmates)
print(len(classmates))
print(classmates[0])
print(classmates[1])
print(classmates[-1])
print(classmates[-2])

classmates.append('kewu')  # 在末尾追加元素
print(classmates)
classmates.insert(1, 'wuershan')  # 插入指定位置
print(classmates)

classmates.pop()  # 删除末尾元素
classmates.pop(1)  # 删除指定位置的元素
classmates[1] = 'jiangshan'  # 更改指定位置的元素

L = [1, '2', True]  # 可以是不同类型
p = ['asp', 'jsp']
g = ['java', 'python', p]   # 可以是list里面包含list

L = []
print(len(L))

classmates = ('kewu', 'lifeng', 'yingying')  # tuple和list非常类似，但是tuple一旦初始化就不能修改
print(classmates[1])  # 没有inert append之类的方法，因为代码不可变所以更安全
print(classmates[-1])
p = ()
print(len(p))
g = (1)  # 定义的不是tuple，是1这个数, 提示去掉多余的圆括号
print(g)

g = (1,)  # 定义了一个tuple，包含最后一个逗号
print(g)
print(len(g))


# ‘可变的’ tuple
t = (1, 2, 3, ['2', '3'])
t[3].append('6')
t[3][1] = '9'
print(t)
print('''
表面上看，tuple的元素确实变了，但其实变的不是tuple的元素，而是list的元素。
tuple一开始指向的list并没有改成别的list，
所以，tuple所谓的“不变”是说，tuple的每个元素，指向永远不变。
即指向'a'，就不能改成指向'b'，指向一个list，就不能改成指向其他对象，
但指向的这个list本身是可变的！
''')


# if conditions

age = 19
if age < 6:
    print('child')
elif age < 18:
    print('teenger')
elif age < 40:
    print('adult')
else:
    print('old')

# birth = input('birth:')
birth = int('1234')  # 需要强制类型转换，input默认输入的是字符串类型
if birth < 2000:
    print('00前')
else:
    print('00后')

bmi = 80.5 / (1.75*1.75)
if bmi < 18.5:
    print('低于18.5:过轻')
elif 18.5 <= bmi < 25:
    print('18.5-25:正常')
elif 25 <= bmi < 28:
    print('25-28：过重')
elif 28 <= bmi < 32:
    print('28-32：肥胖')
else:
    print('高于32：严重肥胖')

# 循环语句
classmates = ['kewu', 'yingying', 'lifeng', 'suyao']
for name in classmates:
    print(name)
sum1 = 0
for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    sum1 += x
print(sum1)

lst = list(range(5))  # range生成从0开始的整数序列
for x in lst:
    print(x)

sum1 = 0
n = 1
while n < 100:
    sum1 = sum1 + n
    n += 2
print(sum1)

L = ['kewu', 'yingying', 'suyao', 'lifeng']
for x in L:
    print('Hello ', x)

n = 0
while n < 100:
    n += 1
    if n == 10:
        continue
    if n == 20:
        break
    print(n)


# dict 用空间换时间，有单独的空间存储索引  dict的key不能重复
p = {'kewu': 20, 'lifeng': 25, 'suyao': 30}
print(p['suyao'])

p['kewu'] = 50
print(p)

if 'kewu' in p:      # 用in判断是否一个key存在于dict中
    print(p['kewu'])
else:
    print('kewu不存在')

if p.get('jiangshan'):  # 用get判断是否一个key存在于dict中
    print('jiangshan存在')
else:
    print('jiangshan不存在')

print(p)
p.pop('kewu')      # 删除一个元素
print(p)


# set 是一组key的集和，但不存储value，里面的key不能重复，要创建一个set，需要提供一个list作为输入集合：
s = set([1, 2, 3, 4, 5])
print(s)

s.add(6)  # 增加key
s.remove(2)  # 删除key
print(s)

# set可以看成数学意义上的无序和无重复元素的集合，因此，两个set可以做数学意义上的交集、并集等操作：

s1 = set(['1', '2', '3', '4'])
s2 = set(['2', '4'])

print(s1 & s2)   # 交集
print(s1 | s2)  # 并集

a = ['a', 'b', 't', 'g']   # list是可变对象
a.sort()
print(a)

a = 'abc'  # 字符串是不可变对象
print(a.replace('a', 'A'))  # replace后生成一个新的对象
print(a)

p = ('6', '7', '8')      # 作为不可变对象的tuple，
a = set([1, 2, 3, 4, 5])
a.add(p)
print(a)

d = {'g': 1, 'b': 2, 'c': 3, 'e': p, p: 9}
print(d)
