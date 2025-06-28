# pi_calculator.py

import decimal
import time

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
    decimal.getcontext().prec = digits + 3

    a = decimal.Decimal(1)
    b = decimal.Decimal(1) / decimal.Decimal(2).sqrt()
    t = decimal.Decimal(1) / decimal.Decimal(4)
    p = decimal.Decimal(1)

    # a_old 用于判断计算是否已经收敛
    a_old = a

    # 循环直到结果收敛
    while True:
        a_next = (a + b) / 2
        b = (a * b).sqrt()
        t -= p * (a - a_next) ** 2
        p *= 2
        a = a_next

        # 当 a 的值不再变化时，说明已达到当前精度下的最大准确度
        if a == a_old:
            break
        a_old = a

    pi_val = (a + b) ** 2 / (4 * t)
    
    # 将结果转换为字符串，并截取到需要的长度
    # +2 是因为 '3.' 占了两个字符位
    return str(pi_val)[:digits + 2]

def main():
    """程序主入口"""
    try:
        input_digits = input("请输入您想计算的 π 的小数位数: ")
        num_digits = int(input_digits)

        print(f"\n开始计算 π 到小数点后 {num_digits} 位...")
        start_time = time.time()

        pi_result = calculate_pi(num_digits)

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
