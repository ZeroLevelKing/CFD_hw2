import numpy as np
import matplotlib.pyplot as plt
from func import diff1, diff2, diff3, diff4, f3, df3, d2f3, g, dg, d2g
import matplotlib

# 设置全局中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams.update({
    'figure.autolayout': True,    # 自动调整布局
    'figure.titlesize': 14,       # 总标题大小
    'axes.labelsize': 12,         # 坐标轴标签大小
    'legend.fontsize': 10,        # 图例字体大小
    'xtick.labelsize': 10,        # X轴刻度标签
    'ytick.labelsize': 10         # Y轴刻度标签
})

# 定义每个差分方法的独立步长列表
h_values_config = {
    # 一阶导数方法
    diff1: [1 / 2**i for i in range(1, 10)],   
    diff2: [1 / 2**i for i in range(5, 15)],  
    # 二阶导数方法
    diff3: [1 / 2**i for i in range(5, 15)],   
    diff4: [1 / 2**i for i in range(1, 10)]   
}

x = 1.0  # 测试点
k = 0.1 

# 一阶导数差分格式验证
du_diff_funcs = [diff1, diff2]
du_tests = [
    (f3, df3, '三次函数 $f_3=x^3-2x^2+3x+1$'),
    (lambda x: g(k, x), lambda x: dg(k, x), '三角函数 $sin(kx)$')
]

plt.figure(figsize=(12, 8))
for idx, diff_func in enumerate(du_diff_funcs, 1):
    plt.subplot(2, 2, idx)
    h_values = h_values_config[diff_func]  # 获取当前方法的步长列表
    for u_func, exact_du, label in du_tests:
        errors = []
        for h in h_values:
            d_approx = diff_func(u_func, x, h)
            d_exact = exact_du(x)
            error = abs(d_approx - d_exact)
            errors.append(error if error > 1e-14 else 1e-14)
        
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
    (f3, d2f3, '三次函数 $f_3=x^3-2x^2+3x+1$'),
    (lambda x: g(k, x), lambda x: d2g(k, x), '三角函数 $sin(kx)$')
]

plt.figure(figsize=(12, 8))
for idx, diff_func in enumerate(d2u_diff_funcs, 1):
    plt.subplot(2, 2, idx)
    h_values = h_values_config[diff_func]  # 获取当前方法的步长列表
    for u_func, exact_d2u, label in d2u_tests:
        errors = []
        for h in h_values:
            d2_approx = diff_func(u_func, x, h)
            d2_exact = exact_d2u(x)
            error = abs(d2_approx - d2_exact)
            errors.append(error if error > 1e-14 else 1e-14)
        
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