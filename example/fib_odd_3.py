from example.fib_odd_1 import is_odd


def fib_list(k):
    assert(k > 0)

    a, b = 0, 1
    ret = []
    for i in range(k):
        print(i)
        a, b = b, a + b
        ret.append(a)

    return ret


def filter_fib(k, p):
    return [i for i in fib_list(k) if is_odd(i) and i <= p]


# 查询 k 个斐波那契函数内 奇数 , 且数字不能大于 p 的和
# 每次都必须获取k个斐波那契函数，有多余的计算
def fib_odd(k, p):
    return sum(filter_fib(k, p))


x = fib_odd(20, 100)
print(x)
