import numpy as np
import matplotlib.pyplot as plt
from func import diff1, diff2, diff3, diff4,f1,f2,f3,df1,df2,df3,d2f1,d2f2,d2f3,g,dg,d2g
import matplotlib

# 设置全局中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  

# 调整默认布局参数防止标签重叠
plt.rcParams.update({
    'figure.autolayout': True,    # 自动调整布局
    'figure.titlesize': 14,       # 总标题大小
    'axes.labelsize': 12,         # 坐标轴标签大小
    'legend.fontsize': 10,        # 图例字体大小
    'xtick.labelsize': 10,        # X轴刻度标签
    'ytick.labelsize': 10         # Y轴刻度标签
})


# 定义不同步长
h_values = [0.1 / (2**i) for i in range(5)]  # [0.1, 0.05, 0.025, 0.0125, 0.00625]
x = 1.0  # 测试点
k = 1.0  

# 一阶导数差分格式验证
du_diff_funcs = [diff1, diff2]
du_tests = [
    (f1, df1, '线性函数 $f_1=2x+1$'),
    (f2, df2, '二次函数 $f_2=3x^2+2x+1$'),
    (f3, df3, '三次函数 $f_3=x^3-2x^2+3x+1$'),
    (lambda x: g(k, x), lambda x: dg(k, x), '三角函数 $sin(kx)$')
]

plt.figure(figsize=(12, 8))
for idx, diff_func in enumerate(du_diff_funcs, 1):
    plt.subplot(2, 2, idx)
    for u_func, exact_du, label in du_tests:
        errors = []
        for h in h_values:
            d_approx = diff_func(u_func, x, h)
            d_exact = exact_du(x)
            error = abs(d_approx - d_exact)
            errors.append(error)  
        
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
    (f1, d2f1, '线性函数 $f_1=2x+1$'),  
    (f2, d2f2, '二次函数 $f_2=3x^2+2x+1$'),
    (f3, d2f3, '三次函数 $f_3=x^3-2x^2+3x+1$'),
    (lambda x: g(k, x), lambda x: d2g(k, x), '三角函数 $sin(kx)$')
]

plt.figure(figsize=(12, 8))
for idx, diff_func in enumerate(d2u_diff_funcs, 1):
    plt.subplot(2, 2, idx)
    for u_func, exact_d2u, label in d2u_tests:
        errors = []
        for h in h_values:
            d2_approx = diff_func(u_func, x, h)
            d2_exact = exact_d2u(x)
            error = abs(d2_approx - d2_exact)
            errors.append(error)
        
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