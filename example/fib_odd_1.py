count = 0

def fib_count():
    global count
    count += 1

def is_odd(n):
    return n % 2


def fib(k):
    assert(k > 0)

    a, b = 0, 1
    for i in range(k):
        a, b = b, a + b
    return a

# 重复计算很多
# 查询 k 个斐波那契函数内 奇数 的和
def fib_odd(k):
    sum = 0
    for i in range(1, k+1):
        num = fib(i)
        if is_odd(num):
           sum += num
    return sum



if __name__ == '__main__':
    x = fib_odd(10)
    print(x)

