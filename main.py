# pi_calculator.py

import decimal
import time
import math

# 在文件顶部检查可选的高性能库 gmpy2 是否存在
try:
    import gmpy2
    GMPY2_AVAILABLE = True
except ImportError:
    GMPY2_AVAILABLE = False

def _gauss_legendre_core(ctx, progress_prefix=""):
    """
    高斯-勒让德算法的核心实现。
    这是一个内部辅助函数，不应直接调用。

    Args:
        ctx (object): 一个提供数学运算的对象 (可以是 decimal 模块或 gmpy2 模块)。
        progress_prefix (str): 迭代进度信息的前缀。

    Returns:
        计算出的π值 (类型取决于传入的ctx)。
    """
    # 使用更具描述性的变量名，以符合代码规范并提高可读性
    term_a = ctx.Decimal(1) if hasattr(ctx, 'Decimal') else ctx.mpfr(1)
    term_b = (ctx.Decimal(1) / ctx.Decimal(2).sqrt()) if hasattr(ctx, 'Decimal') else (1 / ctx.sqrt(ctx.mpfr(2)))
    term_t = ctx.Decimal('0.25') if hasattr(ctx, 'Decimal') else ctx.mpfr(0.25)
    term_p = ctx.Decimal(1) if hasattr(ctx, 'Decimal') else ctx.mpfr(1)

    a_old = term_a
    iteration = 0
    while True:
        iteration += 1
        print(f"\r{progress_prefix}正在进行第 {iteration} 轮迭代...", end="", flush=True)

        a_next = (term_a + term_b) / 2
        term_b = (term_a * term_b).sqrt() if hasattr(ctx, 'Decimal') else ctx.sqrt(term_a * term_b)
        term_t -= term_p * (term_a - a_next) ** 2
        term_p *= 2
        term_a = a_next

        if term_a == a_old:
            print()
            break
        a_old = term_a

    return (term_a + term_b) ** 2 / (4 * term_t)

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
    pi_val = _gauss_legendre_core(decimal)
    # 将结果转换为字符串，并截取到需要的长度
    # +2 是因为 '3.' 占了两个字符位
    return str(pi_val)[:digits + 2]

# 只有在 gmpy2 库可用时，才定义这个高速计算函数
if GMPY2_AVAILABLE:
    def calculate_pi_gmpy2(digits: int) -> str:
        """
        使用 gmpy2 和高斯-勒让德算法高速计算π。
        gmpy2 是C语言库GMP的Python封装，性能极高。

        Args:
            digits: 需要计算的π的小数位数。

        Returns:
            一个字符串，表示计算出的π值。
        """
        if not isinstance(digits, int) or digits <= 0:
            raise ValueError("位数必须是一个正整数。")

        # gmpy2 使用 bits 作为精度单位，而不是十进制位数。
        # log2(10) ≈ 3.322. 增加一些保护位以确保精度。
        bits = int(digits * math.log2(10)) + 16
        gmpy2.get_context().precision = bits
        pi_val = _gauss_legendre_core(gmpy2, progress_prefix="[高速模式] ")
        return str(pi_val)[:digits + 2]

def main():
    """程序主入口"""
    # 在 try 块之前初始化，以避免在 except 块中出现 'used-before-assignment' 警告
    input_digits = ""
    # 将所有主要逻辑都放在一个 try...except 块中，以便统一处理错误
    try:
        # 1. 根据 gmpy2 是否可用，选择合适的计算函数
        if GMPY2_AVAILABLE:
            pi_calculator = calculate_pi_gmpy2
            print("检测到 'gmpy2' 库，将使用高速模式进行计算。")
        else:
            pi_calculator = calculate_pi
            print("\n警告: 未检测到 'gmpy2' 库。")
            print("为了获得数量级的性能提升，建议安装: pip install gmpy2")
            print("正在使用内置的 decimal 模块进行计算（速度较慢）。")

        # 2. 获取用户输入
        input_digits = input("\n请输入您想计算的 π 的小数位数: ")
        num_digits = int(input_digits)

        # 3. 执行计算并计时
        print(f"\n开始计算 π 到小数点后 {num_digits} 位...")
        start_time = time.time()
        pi_result = pi_calculator(num_digits)
        end_time = time.time()
        duration = end_time - start_time

        # 4. 输出结果
        print("\n计算完成！")
        print(f"耗时: {duration:.4f} 秒")
        print(f"\nπ ≈ {pi_result}")

    # 5. 统一处理可能发生的错误
    except ValueError as e:
        # 区分是 int() 转换失败还是我们主动抛出的 ValueError，给出更友好的提示
        if "invalid literal for int()" in str(e):
            print(f"\n错误: 输入无效 '{input_digits}'。请输入一个纯数字的正整数。")
        else:
            print(f"\n错误: {e}")
    except Exception as e:
        print(f"\n发生未知错误: {e}")

if __name__ == "__main__":
    main()
