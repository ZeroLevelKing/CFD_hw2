import numpy as np
import matplotlib.pyplot as plt
from func import diff1, diff2, diff3, diff4, f3, df3, d2f3, g, dg, d2g

# 设置全局中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams.update({
    'figure.autolayout': True,
    'figure.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10
})

# 精度类型配置
dtype_config = {
    'double': np.float64,
    'float': np.float32
}

# 修改后的差分方法，支持不同精度
def diff_with_precision(diff_func, u_func, x, h, dtype):
    x = dtype(x)
    h = dtype(h)
    return diff_func(lambda x: np.array(u_func(x), dtype=dtype), x, h)

# 测试函数包装器
def wrap_functions(u_func, exact_du, dtype):
    return (lambda x: u_func(dtype(x)),
            lambda x: exact_du(dtype(x)),
            f'{u_func.__name__} ({dtype.__name__})')

# 误差分析函数
def analyze_errors(diff_func, u_func, exact_du, x, h_values, dtype):
    errors = []
    for h in h_values:
        d_approx = diff_with_precision(diff_func, u_func, x, h, dtype)
        d_exact = exact_du(dtype(x))
        error = abs(d_approx - d_exact)
        errors.append(max(error, np.finfo(dtype).eps))  # 防止误差为0
    return np.array(errors, dtype=dtype)

x = 1.0  # 测试点
k = 0.1

# 配置差分方法和对应的步长
configs = [
    {
        'title': '一阶导数方法对比',
        'diff_funcs': [diff1, diff2],
        'h_ranges': {
            diff1: [1/np.power(2, i) for i in range(1, 15)],
            diff2: [1/np.power(2, i) for i in range(1, 50)]
        },
        'test_cases': [
            (f3, df3, '三次函数 $f_3$'),
            (lambda x: np.sin(k*x), lambda x: k*np.cos(k*x), r'$\sin(kx)$')
        ]
    },
    {
        'title': '二阶导数方法对比',
        'diff_funcs': [diff3, diff4],
        'h_ranges': {
            diff3: [1/np.power(2, i) for i in range(1, 15)],
            diff4: [1/np.power(2, i) for i in range(1, 10)]
        },
        'test_cases': [
            (f3, d2f3, '三次函数 $f_3$'),
            (lambda x: np.sin(k*x), lambda x: -k**2*np.sin(k*x), r'$\sin(kx)$')
        ]
    }
]

# 生成对比图
for config in configs:
    plt.figure(figsize=(14, 8))
    plt.suptitle(config['title'] + ' - 单双精度对比', y=1.02)
    
    for idx, diff_func in enumerate(config['diff_funcs'], 1):
        ax = plt.subplot(2, 2, idx)
        h_values = config['h_ranges'][diff_func]
        
        # 对每个测试案例进行精度对比
        for u_func, exact_du, label in config['test_cases']:  # 改为解包三个元素
            # 双精度计算
            errors_double = analyze_errors(diff_func, u_func, exact_du, x, h_values, np.float64)
    
            # 单精度计算
            errors_float = analyze_errors(diff_func, u_func, exact_du, x, h_values, np.float32)

            # 绘制双精度结果
            log_h = np.log(h_values)
            log_err = np.log(errors_double)
            slope, _ = np.polyfit(log_h[:len(h_values)//2], log_err[:len(h_values)//2], 1)
            line, = ax.loglog(h_values, errors_double, 'o-', 
                     markersize=4, 
                     label=f'双精度 {label}\n理论收敛阶: {abs(slope):.2f}')
            
            # 绘制单精度结果
            log_err_float = np.log(errors_float)
            slope_float, _ = np.polyfit(log_h[:10], log_err_float[:10], 1)
            ax.loglog(h_values, errors_float, 's--', 
                color=line.get_color(),
                markersize=4,
                alpha=0.7,
                label=f'单精度 {label}\n有效收敛阶: {abs(slope_float):.2f}')
                 
        ax.set_xlabel('步长 h')
        ax.set_ylabel('绝对误差')
        ax.set_title(f'{diff_func.__name__} 误差分析')
        ax.legend(loc='best')
        ax.grid(True, which='both', linestyle='--')
        ax.set_ylim(top=1e2, bottom=1e-16)  # 设置统一的y轴范围

    plt.tight_layout()
    plt.show()