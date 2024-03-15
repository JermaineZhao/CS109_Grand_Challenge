import numpy as np
from scipy.optimize import minimize
from scipy.stats import t


# 综合函数：计算特定周小时数下的可能遇到的crush数量的概率
def calculate_probability(weekly_hour, crush_100):
    target_probs = np.array([3 / 300, 13 / 300, 3 / 300])
    x_values = np.array([5, 15, 25])

    # 内部损失函数
    def loss(params):
        nu, mu, sigma = params
        calculated_probs = t.pdf(x_values, df=nu, loc=mu, scale=sigma)
        return np.sum((calculated_probs - target_probs) ** 2)

    initial_guess = [1, 15, 10]  # 初始参数猜测
    bounds = [(1, 30), (10, 20), (1, 20)]  # 参数边界

    result = minimize(loss, initial_guess, bounds=bounds)  # 寻找最优参数
    optimized_params = result.x

    # 计算给定周小时数下的概率
    nu, mu, sigma = optimized_params
    probability = t.pdf(weekly_hour, df=nu, loc=mu, scale=sigma)

    return probability * 30 * crush_100  # 根据遇到的crush数量调整概率


def main():
    crush_100_input = input("How many crushes will you probably meet on average in 100 opposite sex? ")
    try:
        crush_100 = int(crush_100_input)
        if crush_100 <= 100:
            print(f"You will probably meet {crush_100} crushes on average in 100 opposite sex.")
            weekly_hour_input = input("Enter weekly hours: ")
            weekly_hour = int(weekly_hour_input)

            probability = calculate_probability(weekly_hour, crush_100)
            print(f"Probability: {probability}")

        else:
            print("Please enter a number less than or equal to 100.")
    except ValueError:
        print("Please enter a valid number.")


if __name__ == "__main__":
    main()
