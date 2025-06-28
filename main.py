# pi_calculator.py

import decimal
import time
import math

def calculate_pi(digits: int) -> str:
    """
    使用高斯-勒让德算法计算π到指定的位数。

    Args:
        digits: 需要计算的π的小数位数。

    Returns:
        一个字符串，表示计算出的π值。
    """
    if not isinstance(digits, int) or digits <= 0:
        raise ValueError("位数必须是一个正整数。")

    # decimal的精度(prec)指的是总有效数字位数，
    # 包括小数点前的 '3' 和为了精确计算所需的额外几位。
    # 设置为 digits + 3 是一个比较安全的选择。
    decimal.getcontext().prec = digits + 5 # 增加一点保护位

    a = decimal.Decimal(1)
    b = decimal.Decimal(1) / decimal.Decimal(2).sqrt()
    t = decimal.Decimal(1) / decimal.Decimal(4)
    p = decimal.Decimal(1)

    # a_old 用于判断计算是否已经收敛
    a_old = a
    iteration = 0

    # 循环直到结果收敛
    while True:
        iteration += 1
        # 增加一个实时进度反馈，这样在长时间计算时用户能看到程序在运行
        # \r 让光标回到行首，end=""避免换行，flush=True确保立即显示
        print(f"\r正在进行第 {iteration} 轮迭代...", end="", flush=True)

        a_next = (a + b) / 2
        b = (a * b).sqrt()
        t -= p * (a - a_next) ** 2
        p *= 2
        a = a_next

        # 当 a 的值不再变化时，说明已达到当前精度下的最大准确度
        if a == a_old:
            print() # 迭代结束后换行，保持输出整洁
            break
        a_old = a

    pi_val = (a + b) ** 2 / (4 * t)
    
    # 将结果转换为字符串，并截取到需要的长度
    # +2 是因为 '3.' 占了两个字符位
    return str(pi_val)[:digits + 2]

def calculate_pi_gmpy2(digits: int) -> str:
    """
    使用 gmpy2 和高斯-勒让德算法高速计算π。
    gmpy2 是C语言库GMP的Python封装，性能极高。

    Args:
        digits: 需要计算的π的小数位数。

    Returns:
        一个字符串，表示计算出的π值。
    """
    import gmpy2

    if not isinstance(digits, int) or digits <= 0:
        raise ValueError("位数必须是一个正整数。")

    # gmpy2 使用 bits 作为精度单位，而不是十进制位数。
    # log2(10) ≈ 3.322. 增加一些保护位以确保精度。
    bits = int(digits * math.log2(10)) + 16
    gmpy2.get_context().precision = bits

    a = gmpy2.mpfr(1)
    b = 1 / gmpy2.sqrt(gmpy2.mpfr(2))
    t = gmpy2.mpfr(0.25)
    p = gmpy2.mpfr(1)

    a_old = a
    iteration = 0
    while True:
        iteration += 1
        print(f"\r[高速模式] 正在进行第 {iteration} 轮迭代...", end="", flush=True)

        a_next = (a + b) / 2
        b = gmpy2.sqrt(a * b)
        t -= p * (a - a_next)**2
        p *= 2
        a = a_next

        if a == a_old:
            print() # 迭代结束后换行
            break
        a_old = a

    pi_val = (a + b)**2 / (4 * t)
    return str(pi_val)[:digits + 2]

def main():
    """程序主入口"""
    try:
        # 检测是否安装了 gmpy2，并选择合适的计算函数
        import gmpy2
        pi_calculator = calculate_pi_gmpy2
        print("检测到 'gmpy2' 库，将使用高速模式进行计算。")
    except ImportError:
        pi_calculator = calculate_pi
        print("\n警告: 未检测到 'gmpy2' 库。")
        print("为了获得数量级的性能提升，建议安装: pip install gmpy2")
        print("正在使用内置的 decimal 模块进行计算（速度较慢）。")

    try:
        input_digits = input("请输入您想计算的 π 的小数位数: ")
        num_digits = int(input_digits)

        print(f"\n开始计算 π 到小数点后 {num_digits} 位...")
        start_time = time.time()

        pi_result = pi_calculator(num_digits)

        end_time = time.time()
        duration = end_time - start_time

        print("\n计算完成！")
        print(f"耗时: {duration:.4f} 秒")
        print(f"\nπ ≈ {pi_result}")

    except ValueError as e:
        print(f"\n错误: 输入无效。请输入一个正整数。({e})")
    except Exception as e:
        print(f"\n发生未知错误: {e}")

if __name__ == "__main__":
    main()
