
def fib(x):
    """斐波那契数列计算
    输入x：个数
    输出y：当前个数
    """
    print("enter fib(",x,")")
    if (x==0) or (x==1):
        return 1
    else:
        return fib(x-1)+fib(x-2)

sum = 0

for i in range(12):
    print (i,":",fib(i))
    sum += fib(i)

print ('sum:', sum)