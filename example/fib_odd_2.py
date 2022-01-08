# 查询 10条 订单，时间在 xxxx ,
from example.fib_odd_1 import is_odd


# 计算斐波那契，过滤,累加代码都在写一起，
# 后续维护每加一个步骤代码都堆叠在一起，可读性很差
def fib_odd_2(k):
    assert(k > 0)

    a, b = 0, 1
    sum = 0
    for i in range(k):
        a, b = b, a + b
        if is_odd(a):
            sum += a
    return sum


x = fib_odd_2(10)
print(x)