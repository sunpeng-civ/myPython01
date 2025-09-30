#include <stdio.h>
#include <stdlib.h>

// 函数原型声明
double** allocate_matrix(int rows, int cols);
void free_matrix(double** matrix, int rows);
void read_matrix_data(double** matrix, int rows, int cols, const char* name);
void print_matrix(double** matrix, int rows, int cols, const char* name);
void multiply_matrices(double** A, double** B, double** C, int r1, int c1, int c2);

int main() {
    int r1, c1, r2, c2; // r1, c1: 矩阵A的行和列; r2, c2: 矩阵B的行和列

    // 1. 获取矩阵A的维度
    printf("请输入矩阵 A 的行数和列数 (用空格分隔): ");
    while (scanf("%d %d", &r1, &c1) != 2 || r1 <= 0 || c1 <= 0) {
        printf("输入无效。请输入两个用空格分隔的正整数: ");
        // 清除输入缓冲区，防止无限循环
        int c;
        while ((c = getchar()) != '\n' && c != EOF);
    }

    // 2. 获取矩阵B的维度
    printf("请输入矩阵 B 的行数和列数 (用空格分隔): ");
    while (scanf("%d %d", &r2, &c2) != 2 || r2 <= 0 || c2 <= 0) {
        printf("输入无效。请输入两个用空格分隔的正整数: ");
        // 清除输入缓冲区，防止无限循环
        int c;
        while ((c = getchar()) != '\n' && c != EOF);
    }

    // 3. 检查乘法的前提条件
    if (c1 != r2) {
        printf("错误：矩阵 A 的列数 (%d) 必须等于矩阵 B 的行数 (%d)。\n", c1, r2);
        return 1; // 返回错误码
    }

    // 4. 为矩阵分配内存
    double** A = allocate_matrix(r1, c1);
    double** B = allocate_matrix(r2, c2);
    double** C = allocate_matrix(r1, c2); // 结果矩阵C的维度是 r1 x c2

    // 检查内存分配是否成功
    if (A == NULL || B == NULL || C == NULL) {
        printf("错误：内存分配失败。\n");
        // 释放已成功分配的内存
        free_matrix(A, r1);
        free_matrix(B, r2);
        free_matrix(C, r1);
        return 1;
    }

    // 5. 读取矩阵数据
    read_matrix_data(A, r1, c1, "A");
    read_matrix_data(B, r2, c2, "B");

    // 6. 执行矩阵乘法
    multiply_matrices(A, B, C, r1, c1, c2);

    // 7. 打印输入和输出矩阵
    print_matrix(A, r1, c1, "输入矩阵 A");
    print_matrix(B, r2, c2, "输入矩阵 B");
    print_matrix(C, r1, c2, "结果矩阵 C = A * B");

    // 8. 释放所有动态分配的内存
    free_matrix(A, r1);
    free_matrix(B, r2);
    free_matrix(C, r1);

    return 0; // 程序成功结束
}

/**
 * @brief 为一个 double 类型的矩阵动态分配内存
 * @param rows 矩阵的行数
 * @param cols 矩阵的列数
 * @return 成功则返回指向矩阵的指针，失败则返回 NULL
 */
double** allocate_matrix(int rows, int cols) {
    if (rows <= 0 || cols <= 0) return NULL;

    double** matrix = (double**)malloc(rows * sizeof(double*));
    if (matrix == NULL) {
        return NULL;
    }

    for (int i = 0; i < rows; i++) {
        matrix[i] = (double*)malloc(cols * sizeof(double));
        if (matrix[i] == NULL) {
            // 如果中途分配失败，需要释放已经分配的部分
            for (int j = 0; j < i; j++) {
                free(matrix[j]);
            }
            free(matrix);
            return NULL;
        }
    }
    return matrix;
}

/**
 * @brief 释放动态分配的矩阵内存
 * @param matrix 要释放的矩阵
 * @param rows 矩阵的行数
 */
void free_matrix(double** matrix, int rows) {
    if (matrix == NULL) return;
    for (int i = 0; i < rows; i++) {
        free(matrix[i]); // 释放每一行
    }
    free(matrix); // 释放行指针数组
}

/**
 * @brief 从标准输入读取矩阵的元素
 * @param matrix 要填充数据的矩阵
 * @param rows 矩阵的行数
 * @param cols 矩阵的列数
 * @param name 矩阵的名称，用于提示信息
 */
void read_matrix_data(double** matrix, int rows, int cols, const char* name) {
    printf("请输入矩阵 %s 的元素 (%d x %d):\n", name, rows, cols);
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("  元素 (%d, %d): ", i + 1, j + 1);
            // 循环直到成功读取一个 double
            while (scanf("%lf", &matrix[i][j]) != 1) {
                printf("  输入无效。请输入一个数字: ");
                // 清除输入缓冲区中的无效输入
                int c;
                while ((c = getchar()) != '\n' && c != EOF);
            }
        }
    }
}

/**
 * @brief 将矩阵的元素格式化打印到标准输出
 * @param matrix 要打印的矩阵
 * @param rows 矩阵的行数
 * @param cols 矩阵的列数
 * @param name 矩阵的名称，用于标题
 */
void print_matrix(double** matrix, int rows, int cols, const char* name) {
    printf("\n--- %s ---\n", name);
    if (matrix == NULL) {
        printf("  (矩阵为 NULL)\n");
        return;
    }
    for (int i = 0; i < rows; i++) {
        printf("| ");
        for (int j = 0; j < cols; j++) {
            printf("%8.2f ", matrix[i][j]);
        }
        printf("|\n");
    }
}

/**
 * @brief 计算两个矩阵的乘积 C = A * B
 * @param A 左矩阵
 * @param B 右矩阵
 * @param C 结果矩阵
 * @param r1 矩阵A的行数
 * @param c1 矩阵A的列数 (等于矩阵B的行数)
 * @param c2 矩阵B的列数
 */
void multiply_matrices(double** A, double** B, double** C, int r1, int c1, int c2) {
    // r1: A的行数, c1: A的列数 (B的行数), c2: B的列数
    for (int i = 0; i < r1; i++) {        // 遍历结果矩阵C的行
        for (int j = 0; j < c2; j++) {    // 遍历结果矩阵C的列
            C[i][j] = 0.0; // 初始化结果元素为0
            for (int k = 0; k < c1; k++) { // 计算点积
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}
