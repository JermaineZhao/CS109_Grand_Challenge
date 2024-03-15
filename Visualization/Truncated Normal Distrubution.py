from scipy.stats import norm
import numpy as np

# 第一步：计算 x > -1 时原始正态分布的累积概率
mu = 0  # 均值
x_cutoff = 0 # 可以修改
# 计算累积概率
cumulative_probability = 1 - norm.cdf(x_cutoff, loc=mu, scale=1)  # scale=1 时为标准正态分布

# 第二步：找到符合条件的 sigma
# 首先定义一个函数，用于寻找符合第二个条件的 sigma
def find_sigma():
    # 对于给定的 sigma，计算 x=5 的pdf值是 x=0 的pdf值的20%
    sigma_values = np.linspace(0.1, 10, 10000)  # 创建一个 sigma 值的范围
    for sigma in sigma_values:
        pdf_at_0 = norm.pdf(0, loc=mu, scale=sigma)
        pdf_at_5 = norm.pdf(5, loc=mu, scale=sigma)
        if np.isclose(pdf_at_5, 0.2 * pdf_at_0, atol=1e-3):  # 检查是否接近20%
            return sigma, pdf_at_0, pdf_at_5
    return None, None, None

# 寻找合适的 sigma
sigma, pdf_at_0, pdf_at_5 = find_sigma()

cumulative_probability, sigma, pdf_at_0, pdf_at_5


import matplotlib.pyplot as plt

# 定义正态分布的 x 范围
x = np.linspace(0, 8, 1000)



# 定义积分区间
intervals = [(0, 1), (1, 2),(2, 3),(3, 4),(4, 5),(5, 6),(6, 7),(7, 8)]


# 计算每个区间的积分
integral_values = [norm.cdf(high, loc=mu, scale=sigma) - norm.cdf(low, loc=mu, scale=sigma) for low, high in intervals]

# 计算总和
total = sum(integral_values)

# 缩放数组，使其值加起来为1
scaled_array = [value / total for value in integral_values]



# 使用找到的 sigma 值计算正态分布的 pdf
pdf = norm.pdf(x, loc=mu, scale=sigma)
pdf /= total

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(x, pdf, color='blue', label=f'Normal Distribution\n$\mu=0$, $\sigma={sigma:.2f}$')
plt.title("PDF for Frosh User")
plt.xlabel("Weekly Hour")
plt.ylabel("Probability Density")
plt.xticks(np.arange(0, 8, 1))  # 设置 x 轴刻度
plt.legend()
plt.grid(True)
plt.show()


print(scaled_array)


