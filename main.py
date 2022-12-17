# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import time, turtle

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

    #

A = 1
def printMove(fr, to):
    """
    打印的方式来做移动
    :param fr：开始位置
    :param to: 目标位置
    :return: 
    """
    global A
    print (A,": move from ", str(fr), " to ", str(to))
    A+=1

def MoveTowers (n, fr, to, spare):
    if n == 1:
        printMove(fr, to)
    else:
        MoveTowers(n-1, fr, spare, to)
        MoveTowers(1,fr,to,spare)
        MoveTowers(n-1, spare, to, fr)

MoveTowers(10,1,3,2)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
