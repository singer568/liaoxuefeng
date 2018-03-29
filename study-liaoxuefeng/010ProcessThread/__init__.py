# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""进程与线程"""
__author__='wuershan'

from multiprocessing import Process,Queue
import os,time,random,queue
from multiprocessing import Pool
import subprocess
import  threading
from multiprocessing.managers import BaseManager

'''--------------------------------------------------part1 多进程'''
#fork是linux上专用的，multiprocessing模块就是跨平台版本的多进程模块
print('------------------------------------------------------------------------1')

print('Process (%s) start...' % os.getpid())
# Only works on Unix/Linux/Mac:
pid = os.fork()
if pid == 0:
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))

print('------------------------------------------------------------------------2')
# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()  # join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步。
    print('Child process end.')
print('------------------------------------------------------------------------3')
def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4) # pool的大小默认是cpu的核数
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
# 对Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process了。
# 请注意输出的结果，task 0，1，2，3是立刻执行的，而task 4要等待前面某个task完成后才执行，
# 这是因为Pool的默认大小在我的电脑上是4，因此，最多同时执行4个进程。
# 这是Pool有意设计的限制，并不是操作系统的限制。

print('------------------------------------------------------------------------4')
#很多时候，子进程并不是自身，而是一个外部进程。我们创建了子进程后，还需要控制子进程的输入和输出。
#subprocess模块可以让我们非常方便地启动一个子进程，然后控制其输入和输出。
print('$ nslookup www.python.org')
r = subprocess.call(['nslookup', 'www.python.org'])
print(r)

#如果还需要输入，则通过communicate交互
print('$ nslookup')
p = subprocess.Popen(['nslookup'], stdin = subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
print(output.decode('utf-8'))
print('Exit Code:', p.returncode)

print('------------------------------------------------------------------------5')
def write(q):
    print('Process to write:%s'%os.getpid())
    for value in ['A', 'B','C']:
        print('Put %s to queue.....'%value)
        q.put(value)
        time.sleep(random.random)
def read(q):
    print('Process to read:%s'%os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from Queue.' %value)


if __name__=='__main__':
    q = Queue  #附近城创建queue，然后传给各个子进程
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))

    pw.start() #启动两个子进程
    pr.start()
    pw.join() #等待pw结束
    pr.terminate() #pr死循环
'''--------------------------------------------------part2 多线程'''
def loop():
    print('thread %s is running.....'%threading.current_thread().name)
    n = 0
    while n < 5:
        n = n+1
        print('thread %s >>> %s'%(threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)


# 线程同步锁机制
balance = 0
lock = threading.Lock  #为避免更新balance出错，需要加锁
def change_it(n):
    #先存后取，结果应该为0
    global balance
    balance = balance + n
    balance = balance - n
def run_thread(n):
    for i in range(100000):
        lock.acquire()  #先要获取锁
        try:
            change_it(n)
        finally:
            lock.release() #改完一定要释放锁

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print('balance=',balance)

'''
启动与CPU核心数量相同的N个线程，在4核CPU上可以监控到CPU占用率仅有102%，也就是仅使用了一核。threading.cpu_count()
但是用C、C++或Java来改写相同的死循环，直接可以把全部核心跑满，4核就跑到400%，8核就跑到800%，为什么Python不行呢？

因为Python的线程虽然是真正的线程，但解释器执行代码时，有一个GIL锁：Global Interpreter Lock，任何Python线程执行前，必须先获得GIL锁，然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。这个GIL全局锁实际上把所有线程的执行代码都给上了锁，所以，多线程在Python中只能交替执行，即使100个线程跑在100核CPU上，也只能用到1个核。

GIL是Python解释器设计的历史遗留问题，通常我们用的解释器是官方实现的CPython，要真正利用多核，除非重写一个不带GIL的解释器。

所以，在Python中，可以使用多线程，但不要指望能有效利用多核。如果一定要通过多线程利用多核，那只能通过C扩展来实现，不过这样就失去了Python简单易用的特点。

不过，也不用过于担心，Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。

Python解释器由于设计时有GIL全局锁，导致了多线程无法利用多核。多线程的并发在Python中就是一个美丽的梦。
'''

'''--------------------------------------------------part3 ThreadLocal'''

local_school = threading.local
def process_student():
    std = local_school.student
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))


def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name
    process_student()

t1 = threading.Thread(target= process_thread, args=('Alice',), name='Thread-A')
t2 = threading.Thread(target= process_thread, args=('Bob',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()

'''
全局变量local_school就是一个ThreadLocal对象，每个Thread对它都可以读写student属性，但互不影响。你可以把local_school看成全局变量，
但每个属性如local_school.student都是线程的局部变量，可以任意读写而互不干扰，也不用管理锁的问题，ThreadLocal内部会处理。
可以理解为全局变量local_school是一个dict，不但可以用local_school.student，还可以绑定其他变量，如local_school.teacher等等。
ThreadLocal最常用的地方就是为每个线程绑定一个数据库连接，HTTP请求，用户身份信息等，这样一个线程的所有调用到的处理函数都
可以非常方便地访问这些资源。
'''
'''--------------------------------------------------part4 进程和线程'''
'''
无论是多进程还是多线程，只要数量一多，效率肯定上不去，为什么呢？
多任务一旦多到一个限度，就会消耗掉系统所有的资源，结果效率急剧下降，所有任务都做不好。
计算密集型任务的特点是要进行大量的计算，消耗CPU资源,这种计算密集型任务虽然也可以用多任务完成，但是任务越多，花在任务切换的时间就越多，CPU执行任务的效率就越低，所以，要最高效地利用CPU，计算密集型任务同时进行的数量应当等于CPU的核心数。
计算密集型任务由于主要消耗CPU资源，因此，代码运行效率至关重要。Python这样的脚本语言运行效率很低，完全不适合计算密集型任务。对于计算密集型任务，最好用C语言编写。

第二种任务的类型是IO密集型，涉及到网络、磁盘IO的任务都是IO密集型任务，这类任务的特点是CPU消耗很少，任务的大部分时间都在等待IO操作完成（因为IO的速度远远低于CPU和内存的速度）。对于IO密集型任务，任务越多，CPU效率越高，但也有一个限度。常见的大部分任务都是IO密集型任务，比如Web应用。
IO密集型任务执行期间，99%的时间都花在IO上，花在CPU上的时间很少，因此，用运行速度极快的C语言替换用Python这样运行速度极低的脚本语言，完全无法提升运行效率。对于IO密集型任务，最合适的语言就是开发效率最高（代码量最少）的语言，脚本语言是首选，C语言最差。

如果充分利用操作系统提供的异步IO支持，就可以用单进程单线程模型来执行多任务，这种全新的模型称为事件驱动模型，Nginx就是支持异步IO的Web服务器，它在单核CPU上采用单进程模型就可以高效地支持多任务。在多核CPU上，可以运行多个进程（数量与CPU核心数相同），充分利用多核CPU。由于系统总的进程数量十分有限，因此操作系统调度非常高效。用异步IO编程模型来实现多任务是一个主要的趋势。

对应到Python语言，单线程的异步编程模型称为协程，有了协程的支持，就可以基于事件驱动编写高效的多任务程序。我们会在后面讨论如何编写协程。
'''
'''--------------------------------------------------part5 分布式进程'''
'''
Python的multiprocessing模块不但支持多进程，其中managers子模块还支持把多进程分布到多台机器上
原有的Queue可以继续使用，但是，通过managers模块把Queue通过网络暴露出去，就可以让其他机器的进程访问Queue了。
我们先看服务进程，服务进程负责启动Queue，把Queue注册到网络上，然后往Queue里面写入任务：
'''
task_queue = queue.Queue  # 发送任务的队列
result_queue = queue.Queue # 接收结果的队列
class QueueManager(BaseManager):
    pass
QueueManager.register('get_task_queue', callable=lambda :task_queue) # 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_result_queue', callable=lambda :result_queue)

manager = QueueManager(address=('', 5000), authkey=b'abc') # 绑定端口5000, 设置验证码'abc':
manager.start()
task = manager.get_task_queue()
result = manager.get_result_queue()

# 放几个任务进去:
for i in range(10):
    n = random.randint(0, 10000)
    print('put task %d' %n)
    task.put(n)
# 从result队列读取结果:
print('Try get results.....')
for i in range(10):
    r = result.get(timeout = 10)
    print('Result:%s'%r)

#关闭
manager.shutdown()
print('master exit')

'''
请注意，当我们在一台机器上写多进程程序时，创建的Queue可以直接拿来用，但是，在分布式多进程环境下，
添加任务到Queue不可以直接对原始的task_queue进行操作，那样就绕过了QueueManager的封装，
必须通过manager.get_task_queue()获得的Queue接口添加。
'''
#然后，在另一台机器上启动任务进程（本机上启动也可以）
# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass
# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')
# 连接到服务器，也就是运行task_master.py的机器:
server_addr = '127.0.0.1'
print('Connect to server %s...' % server_addr)
# 端口和验证码注意保持与task_master.py设置的完全一致:
m = QueueManager(address=(server_addr, 5000), authkey=b'abc')
# 从网络连接:
m.connect()
# 获取Queue的对象:
task = m.get_task_queue()
result = m.get_result_queue()
# 从task队列取任务,并把结果写入result队列:
for i in range(10):
    try:
        n = task.get(timeout=1)
        print('run task %d * %d...' % (n, n))
        r = '%d * %d = %d' % (n, n, n*n)
        time.sleep(1)
        result.put(r)
    except Queue.Empty:
        print('task queue is empty.')
# 处理结束:
print('worker exit.')

'''
而Queue之所以能通过网络访问，就是通过QueueManager实现的。由于QueueManager管理的不止一个Queue，所以，要给每个Queue的网络调用接口起个名字，比如get_task_queue。

authkey有什么用？这是为了保证两台机器正常通信，不被其他机器恶意干扰。如果task_worker.py的authkey和task_master.py的authkey不一致，
肯定连接不上。

Python的分布式进程接口简单，封装良好，适合需要把繁重任务分布到多台机器的环境下。

注意Queue的作用是用来传递任务和接收结果，每个任务的描述数据量要尽量小。比如发送一个处理日志文件的任务，就不要发送几百兆的日志文件本身，
而是发送日志文件存放的完整路径，由Worker进程再去共享的磁盘上读取文件。
'''





