from example.fib_odd_1 import is_odd


def fib(k):
    assert(k > 0)
    print("start fib")
    a, b = 0, 1
    for i in range(k):
        print(i)
        a, b = b, a + b
        yield a

# 查询 k 个斐波那契函数内 奇数 , 且数字不能大于 p 的和
# 延迟计算，由最外层控制计算
def filter_fib(k, p):
    for x in fib(k):
        if x > p:
            break
        if is_odd(x):
            yield x


def fib_odd(k, p):
    return sum(filter_fib(k, p))


k, p = 20, 100
# x = filter_fib(k, p)
x = fib_odd(20, 100)
print(x)
