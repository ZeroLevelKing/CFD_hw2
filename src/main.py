import numpy as np
import matplotlib.pyplot as plt
from func import diff1, diff2, diff3, diff4,f1,f2,f3,df1,df2,df3,d2f1,d2f2,d2f3,g,dg,d2g

# 定义不同步长用于验证
h_values = [0.1 / (2**i) for i in range(5)]  # [0.1, 0.05, 0.025, 0.0125, 0.00625]
x = 1.0  # 统一的测试点
k = 1.0  # 三角函数的波数

# 一阶导数差分格式验证
du_diff_funcs = [diff1, diff2]
du_tests = [
    (f1, df1, '线性函数 f1=2x+1'),
    (f2, df2, '二次函数 f2=3x²+2x+1'),
    (f3, df3, '三次函数 f3=x³-2x²+3x+1'),
    (lambda x: g(k, x), lambda x: dg(k, x), '三角函数 sin(kx)')
]

plt.figure(figsize=(12, 8))
for idx, diff_func in enumerate(du_diff_funcs, 1):
    plt.subplot(2, 2, idx)
    for u_func, exact_du, label in du_tests:
        errors = []
        for h in h_values:
            try:
                d_approx = diff_func(u_func, x, h)
            except:
                d_approx = diff_func(u_func, x + h, h)  # 处理diff2在x=0处的边界情况
            d_exact = exact_du(x)
            error = abs(d_approx - d_exact)
            errors.append(error if error != 0 else 1e-16)  # 避免零误差
        
        # 计算收敛阶
        log_h = np.log(h_values)
        log_err = np.log(errors)
        slope, _ = np.polyfit(log_h, log_err, 1)
        
        plt.loglog(h_values, errors, 'o-', label=f'{label}\n收敛阶: {slope:.2f}')
    
    plt.xlabel('步长 h (log scale)')
    plt.ylabel('绝对误差 (log scale)')
    plt.title(f'{diff_func.__name__} 一阶导数精度验证')
    plt.legend()
    plt.grid(True, which='both', linestyle='--')

# 二阶导数差分格式验证
d2u_diff_funcs = [diff3, diff4]
d2u_tests = [
    (f1, d2f1, '线性函数 f1=2x+1'),
    (f2, d2f2, '二次函数 f2=3x²+2x+1'),
    (f3, d2f3, '三次函数 f3=x³-2x²+3x+1'),
    (lambda x: g(1, x), lambda x: d2g(1, x), '三角函数 sin(x)')
]

plt.figure(figsize=(12, 8))
for idx, diff_func in enumerate(d2u_diff_funcs, 1):
    plt.subplot(2, 2, idx)
    for u_func, exact_d2u, label in d2u_tests:
        errors = []
        for h in h_values:
            try:
                d2_approx = diff_func(u_func, x, h)
            except:
                d2_approx = diff_func(u_func, x + h, h)  # 处理边界情况
            d2_exact = exact_d2u(x)
            error = abs(d2_approx - d2_exact)
            errors.append(error if error != 0 else 1e-16)
        
        # 计算收敛阶
        log_h = np.log(h_values)
        log_err = np.log(errors)
        slope, _ = np.polyfit(log_h, log_err, 1)
        
        plt.loglog(h_values, errors, 'o-', label=f'{label}\n收敛阶: {slope:.2f}')
    
    plt.xlabel('步长 h (log scale)')
    plt.ylabel('绝对误差 (log scale)')
    plt.title(f'{diff_func.__name__} 二阶导数精度验证')
    plt.legend()
    plt.grid(True, which='both', linestyle='--')

plt.tight_layout()
plt.show()