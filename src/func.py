from math import sin, pi, cos

# 定义对于du/dx的第一种差分格式
def diff1(u, x, h):
    u0 = u(x)
    u1 = u(x + h)
    return (u1 - u0) / h

# 定义对于du/dx的第二种差分格式
def diff2(u, x, h):
    u_1 = u(x - h)
    u0 = u(x)
    u1 = u(x + h)
    u2 = u(x + 2 * h)
    return (- 2 * u_1  - 3 * u1 + 6 * u0 - u2) / (6 * h )

# 定义对于d^2u/dx^2的第一种差分格式
def diff3(u, x, h):
    u0 = u(x)
    u1 = u(x + h)
    u2 = u(x + 2 * h)
    return (u2 - 2 * u1 + u0) / (h ** 2)

# 定义对于d^2u/dx^2的第二种差分格式
def diff4(u, x, h):
    u_1 = u(x - h)
    u0 = u(x)
    u1 = u(x + h)
    return (u_1 - 2 * u0 + u1) / (h ** 2)

# 用于测试的多项式函数
def f1(x):
    return  2 * x + 1
def f2(x):
    return 3 * x ** 2 + 2 * x + 1
def f3(x):
    return x ** 3 - 2 * x ** 2 + 3 * x + 1
def df1(x):
    return 2
def df2(x):
    return 6 * x + 2
def df3(x):
    return 3 * x ** 2 - 4 * x + 3
def d2f1(x):
    return 0
def d2f2(x):
    return 6
def d2f3(x):
    return 6 * x - 4

# 用于测试的三角函数
def g(k,x):
    return sin(k * x)
def dg(k,x):
    return k * cos(k * x)
def d2g(k,x):
    return - k ** 2 * sin(k * x)