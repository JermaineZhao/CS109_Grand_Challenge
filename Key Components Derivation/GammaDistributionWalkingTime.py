# This file get the expected walking time using Nelder-Mead

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma
from scipy.optimize import minimize
from scipy.optimize import minimize

file_path = '../Gathered Data/Walktime.txt'

# 读取文件并解析数据
with open(file_path, 'r') as file:
    lines = file.readlines()
    # 解析每一行，转换成整数列表
    data_parsed = [list(map(lambda x: int(x.split()[0]), line.strip().split(','))) for line in lines if line.strip()]

    # 转换成numpy数组
all_data = np.array(data_parsed)


# 所有组数据
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

# 给定的目标加权平均值
target_avgs = np.array([11, 13, 6.5, 9, 6.5, 5, 7, 11, 11, 7])

# 定义目标函数：最小化加权平均值与目标值的平方差之和
def objective(params):
    A, B = params
    total_cost = 0
    for i, data in enumerate(ex_data):
        weights = A * np.exp(-B * (data - np.min(data)))
        weights /= np.sum(weights)  # 标准化权重
        weighted_avg = np.sum(weights * data)  # 计算加权平均值
        total_cost += (weighted_avg - target_avgs[i]) ** 2  # 累加平方差
    return total_cost

# 使用优化算法寻找最佳A和B
initial_guess = [1, 0.1]  # 初始猜测
result = minimize(objective, initial_guess, method='Nelder-Mead')

# 输出最优A和B
A_opt, B_opt = result.x
print(A_opt, B_opt)

# 使用找到的最优A和B参数计算权重和加权平均值
weighted_avgs = []

for i, data in enumerate(all_data):
    # 计算权重
    weights = A_opt * np.exp(-B_opt * (data - np.min(data)))
    weights /= np.sum(weights)  # 标准化权重
    # 计算加权平均值
    weighted_avg = np.sum(weights * data)
    weighted_avgs.append(weighted_avg)

print(weighted_avgs)

with open('../User Interface (Main)/Machine_learned_Walktime.txt', 'w') as f:
    for avg in weighted_avgs:
        f.write(str(avg) + '\n')

print("Output data written to 'output_data.txt'.")




# file_path = 'Walktime.txt'
#
# # 读取文件并解析数据
# with open(file_path, 'r') as file:
#     lines = file.readlines()
#     # 解析每一行，转换成整数列表
#     data_parsed = [list(map(lambda x: int(x.split()[0]), line.strip().split(','))) for line in lines if line.strip()]
#
#     # 转换成numpy数组
# data = np.array(data_parsed)

# 提供的数据，每行代表一个上课地点到五个不同dating spot的走路时间
# data = np.array([
#     [26, 15, 9, 8, 5],
#     [25, 16, 10, 9, 5],
#     [25, 17, 10, 9, 5],
#     [29, 12, 7, 12, 3],
#     [29, 12, 6, 12, 4],
#     [27, 11, 7, 10, 6],
#     [25, 12, 9, 8, 6],
#     [24, 13, 10, 7, 7],
#     [25, 14, 10, 7, 6],
#     [29, 11, 5, 11, 4]
# ])
#
# # 估计每个dating spot的Gamma分布参数
# def estimate_gamma_params(data):
#     # 使用最大似然估计来估计Gamma分布的参数
#     # Gamma分布的似然函数并不简单，这里使用scipy的方法进行拟合
#
#     # 存储估计的参数
#     alpha_params = []
#     beta_params = []
#
#     for i in range(data.shape[1]):
#         # 计算每个dating spot的参数
#         a, loc, scale = gamma.fit(data[:, i], floc=0)  # 固定loc为0
#         alpha_params.append(a)
#         beta_params.append(1/scale)  # scipy使用的是scale的倒数
#
#     return np.array(alpha_params), np.array(beta_params)
#
# # 估计参数
# alpha_params, beta_params = estimate_gamma_params(data)
#
# # 绘制Gamma分布
# time_points = np.linspace(0, 30, 1000)  # 创建时间点
# plt.figure(figsize=(12, 8))
#
# for i in range(5):
#     pdf = gamma.pdf(time_points, a=alpha_params[i], scale=1/beta_params[i])
#     plt.plot(time_points, pdf, label=f'Dating Spot {i+1}')
#
# plt.title('Gamma Distribution of Walking Times to Dating Spots')
# plt.xlabel('Time (minutes)')
# plt.ylabel('Probability Density')
# plt.legend()
# plt.show()
#
# alpha_params, beta_params
