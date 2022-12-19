import time


def fib(x):
    """斐波那契数列计算
    输入x：个数
    输出y：当前个数
    """
    if (x == 0) or (x == 1):
        return 1
    else:
        return fib(x - 1) + fib(x - 2)


def fib_effi(n, dd):
    if n in dd:
        return dd[n]
    else:
        ans = fib_effi(n - 1, dd) + fib_effi(n - 2, dd)
        dd[n] = ans
        return ans




time1 = time.time()

sum = 0

for i in range(35):
    sum += fib(i)
time2 = time.time()

print('计算时间:', (time2 - time1))

time1 = time.time()

sum = 0
d = {0:1, 1: 1}
for i in range(35):
    sum += fib_effi(i, d)
time2 = time.time()
print('计算时间:', (time2 - time1))

print('sum:', sum)
