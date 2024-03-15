import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# 示例数据
ex_data = np.array([
    [24, 23, 16, 9, 10],
    [28, 22, 15, 14, 9],
    [9, 11, 5, 19, 9],
    [25, 13, 11, 8, 9],
    [9, 11, 5, 19, 9],
    [18, 19, 16, 1, 13],
    [28, 8, 6, 11, 7],
    [23, 11, 13, 9, 12],
    [9, 11, 5, 19, 9],
    [23, 11, 13, 9, 12]
])

# 目标加权平均值
target_avgs = np.array([11, 13, 6.5, 9, 6.5, 5, 7, 11, 11, 7])

# 跟踪参数值
params_trace = []

# 定义目标函数
def objective(params):
    A, B = params
    total_cost = 0
    for i, data in enumerate(ex_data):
        weights = A * np.exp(-B * (data - np.min(data)))
        weights /= np.sum(weights)
        weighted_avg = np.sum(weights * data)
        total_cost += (weighted_avg - target_avgs[i]) ** 2
    params_trace.append(params)
    return total_cost

# 使用优化算法寻找最佳A和B
initial_guess = [1, 0.1]
result = minimize(objective, initial_guess, method='Nelder-Mead')

# 将迭代过程中的参数值转换为numpy数组以便绘图
params_trace = np.array(params_trace)

# 更新颜色设置
colors = ['red', 'green', 'blue', 'magenta']

# 绘制迭代过程
plt.figure(figsize=(8, 6))
plt.plot(params_trace[:, 0], params_trace[:, 1], 'o-', color='grey', alpha=0.3, label='Iteration Path')

# 选取前几个迭代的点作为示例
num_points_to_show = 12
for i in range(0, num_points_to_show, 3):
    if i+2 < len(params_trace):
        color_index = i // 3
        triangle_color = colors[color_index] if color_index < len(colors) else 'grey'
        triangle = params_trace[i:i+3]
        plt.plot(*np.append(triangle, [triangle[0]], axis=0).T, marker='o', markersize=5, color=triangle_color, label=f'Triangle at Iteration {i//3+1}')

plt.xlabel('A')
plt.ylabel('B')
plt.title('Nelder-Mead Optimization Process')
plt.legend()
plt.show()
