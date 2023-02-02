import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 设置常量
G = 1
M1 = 1
M2 = 1
M3 = 1
dt = 0.01

# 初始化位置和速度
r1 = np.array([1, 0]).astype(np.float64)
v1 = np.array([0, 0.5]).astype(np.float64)
r2 = np.array([-1, 0]).astype(np.float64)
v2 = np.array([0, -0.5]).astype(np.float64)
r3 = np.array([0, 1]).astype(np.float64)
v3 = np.array([-0.5, 0]).astype(np.float64)

r = np.array([r1, r2, r3])
v = np.array([v1, v2, v3])
m = np.array([M1, M2, M3])

# 计算加速度
def acc(r, m):
    a = np.zeros((3, 2))
    for i in range(3):
        for j in range(3):
            if i != j:
                dr = r[j] - r[i]
                a[i] += -m[j] * dr / np.linalg.norm(dr)**3
    return a

# 定义动画函数
def animate(i):
    global r, v
    a = acc(r, m)
    v += a * dt
    r += v * dt
    plt.clf()
    plt.plot(r[0, 0], r[0, 1], 'ro')
    plt.plot(r[1, 0], r[1, 1], 'bo')
    plt.plot(r[2, 0], r[2, 1], 'go')
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    plt.title("Three-Body Simulation")

# 运行动画
ani = FuncAnimation(plt.gcf(), animate, interval=10)
plt.show()
