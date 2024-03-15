from scipy.stats import norm

# 第一个分布的sigma值
sigma_dist1 = 3.06  # 根据之前的计算

def truncated_normal_pdf_dist1(x, sigma=3.06):
    """
    Returns the PDF of the first truncated normal distribution at x,
    with standard deviation sigma, and truncated from below at 0.
    """
    if x <= 0:
        return 0
    else:
        normalization_factor = 1 - norm.cdf(0, scale=sigma)
        return norm.pdf(x, scale=sigma) / normalization_factor

# 示例：绘制第一个分布的PDF
import numpy as np
import matplotlib.pyplot as plt

# 定义x值范围
x_values = np.linspace(0, 10, 1000)  # 从0开始，考虑到截断

# 计算PDF值
pdf_values = [truncated_normal_pdf_dist1(x) for x in x_values]

# 绘制图形
plt.figure(figsize=(8, 4))
plt.plot(x_values, pdf_values, label='Truncated Normal Distribution 1')
plt.fill_between(x_values, pdf_values, alpha=0.2)
plt.title('Truncated Normal Distribution 1 with $\\sigma=3.06$')
plt.xlabel('x')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)
plt.show()
