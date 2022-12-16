# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

import math, time

accu = 0.000000000001
x = eval(input("input num:"))
root_num = eval(input("input root num:"))
if x > 0:
    left = 0
    right = x
else:
    left = x
    right = 0

time1 = time.time()
root = 0

while 1:
    root = float((left + right) / 2)
    if root**root_num > x :
        right = root
    else:
        left = root

    if abs(root**root_num - x ) < accu:
        break
time2 = time.time()
print ("the", root_num, "root of", x, "is ", root )
print ('calc time is ',(time2-time1))


sum = x**2
time3 = time.time()

print ("sqr of10", x ,"is ", sum)

print ('sqr time is ',(time3-time2))

my_text = "China will continue to play its role as president of COP15, closely cooperate with all parties and stakeholders toward the conclusion of the Post-2020 Global Biodiversity Framework and successful completion of all items on COP15's agenda, and contribute to the full attainment of the three main objectives of the Convention on Biological Diversity — conservation, sustainable use and sharing of the benefits of biodiversity, Mao said."
char_count = {c : my_text.count(c) for c in my_text}
print (char_count)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
