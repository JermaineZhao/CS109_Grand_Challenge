from scipy.stats import truncnorm
import numpy as np
import scipy.optimize as opt

# 目标条件
target_ratio = 0.2  # x=6 处的PDF高度是 x=0 处高度的20%
x_6 = 6
x_0 = 0

# 截断正态分布的边界
a, b = 0, np.inf  # x > 0


# 定义目标函数：寻找使 x=6 处的PDF高度是 x=0 处高度20% 的 sigma
def find_sigma(sigma):
    # 截断正态分布的参数
    loc = 0  # miu = 0
    scale = sigma  # sigma未知

    # 截断正态分布对象
    trunc_dist = truncnorm(a=(a - loc) / scale, b=(b - loc) / scale, loc=loc, scale=scale)

    # 计算x=0和x=6处的PDF值
    pdf_x_0 = trunc_dist.pdf(x_0)
    pdf_x_6 = trunc_dist.pdf(x_6)

    # 目标是使 x=6 处的PDF高度是 x=0 处高度的20%
    return pdf_x_6 - target_ratio * pdf_x_0


# 使用优化方法找到合适的sigma值
sigma_opt, = opt.fsolve(find_sigma, x0=1)  # 初始猜测为1

sigma_opt

# 使用之前找到的最优sigma值
sigma = sigma_opt
loc = 0  # miu = 0

# 创建截断正态分布对象
trunc_dist_opt = truncnorm(a=(a - loc) / sigma, b=(b - loc) / sigma, loc=loc, scale=sigma)

# 定义积分区间
intervals = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]

# 计算各个区间的积分（CDF差值）
integrals = [trunc_dist_opt.cdf(high) - trunc_dist_opt.cdf(low) for low, high in intervals]

integrals


import matplotlib.pyplot as plt

# 定义x轴的点，覆盖0到9，用于绘图
x = np.linspace(0, 9, 400)
# 计算这些点的PDF
y = trunc_dist_opt.pdf(x)

# 重新绘制图形，调整x轴的刻度为要求的1到8
plt.figure(figsize=(10, 6))
plt.plot(x, y, color='blue')  # 使用蓝色线条
plt.title("PDF for Freshman User")
plt.xlabel("Age gap with freshman")
plt.ylabel("PDF")
plt.xticks(np.arange(0, 9, 1))  # 设置x轴刻度为1到8
plt.grid(True)

# 显示图形
plt.show()