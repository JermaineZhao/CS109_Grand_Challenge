#

# import numpy as np
#
# # 示例数据：第一个课到第一个dating spot的走路时间
# sample_data = np.array([26, 15, 9, 8, 5])
#
# # Bootstrapping
# bootstrap_samples = 10000
# bootstrap_means = np.empty(bootstrap_samples)
#
# for i in range(bootstrap_samples):
#     bootstrap_sample = np.random.choice(sample_data, size=sample_data.size, replace=True)
#     bootstrap_means[i] = np.mean(bootstrap_sample)
#
# # 计算95%置信区间
# confidence_interval = np.percentile(bootstrap_means, [2.5, 97.5])
#
# print("Bootstrapped 95% confidence interval for the mean:", confidence_interval)
from scipy.interpolate import CubicSpline
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt

# 定义数据点
x = np.array([5, 8, 9, 6, 17.6])  # 时间
x = np.sort(x)
y = np.array([1, 2, 3, 4, 5])    # 到达地点的个数

# 使用样条插值生成平滑曲线
cs = CubicSpline(x, y)

# 绘制样条插值结果和原始数据点
x_new = np.linspace(x.min(), x.max(), 100)
y_new = cs(x_new)

plt.figure(figsize=(8, 6))
plt.plot(x, y, 'o', label='Original data points')
plt.plot(x_new, y_new, label='Cubic Spline interpolation')
plt.xlabel('Time')
plt.ylabel('Number of reached spots')
plt.legend()
plt.title('Smooth Curve Through Data Points')
plt.show()

# 计算曲线下的面积
area, _ = quad(cs, x.min(), x.max())

# 计算平均到达一个地点所需的时间
average_time = area / 5
average_time

print(average_time)