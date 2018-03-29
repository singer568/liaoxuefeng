def _int_iter():  # 生成器生成从3开始的无限奇数序列
    n = 1
    while True:
        n = n + 2
        yield n


def _not_divisible(n):  # 定义筛选函数
    return lambda x: x % n > 0


def primes():
    it = _int_iter()  # 初始序列
    while True:
        n = next(it)  # 返回序列的第一个数
        yield n
        it = filter(_not_divisible(n), it)  # 构造新序列


for n in primes():  # 构造循环条件，使之可以输出任何范围的素数序列
    if n < 1000:
        print(n)
    else:
        break