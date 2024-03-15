# 询问用户在10分钟内能够想出多少条 pickup line
while True:
    pickup_user = input("How many pickup lines can you come up with in 10 minutes? ")
    try:
        pickup_user = int(pickup_user)
        if pickup_user < 0 or pickup_user > 100:
            print("Please enter a number between 0 and 100.")
        else:
            break
    except ValueError:
        print("Please enter a valid number.")

# 询问用户认为这些 pickup line 中有多少是好的
while True:
    good_pickup_user = input(f"How many good pickup lines do you assume to be within the {pickup_user} pickup lines? ")
    try:
        good_pickup_user = int(good_pickup_user)
        if good_pickup_user < 0 or good_pickup_user > pickup_user:
            print(f"Please enter a number between 0 and {pickup_user}.")
        else:
            break
    except ValueError:
        print("Please enter a valid number.")

# 输出结果
print("User's response:")
print("Number of pickup lines user can come up with:", pickup_user)
print("Number of good pickup lines user assumes to be within the pickup lines:", good_pickup_user)



import numpy as np

# 从文本文件中读取时间数据
with open('../Gathered Data/Class_ranking_Location.txt', 'r') as file:
    time_data = [float(line.strip()) for line in file]

lambda_parameter = []


for i in range(len(time_data)):
    lambda_parameter.append(pickup_user * time_data[i] / 10)


poisson_expectation = lambda_parameter
#
# print("Lambda for Poisson distribution:", lambda_parameter)
# print("Expectation of the Poisson distribution:", poisson_expectation)


from scipy.stats import bernoulli, binom

# 模拟好坏 pickup line
p = good_pickup_user / pickup_user
bernoulli_dist = bernoulli(p)

# 计算好 pickup line 和不好 pickup line 的期望
good_pickup_expectation = [p * expectation for expectation in poisson_expectation]
bad_pickup_expectation = [(1 - p) * expectation for expectation in poisson_expectation]


print(good_pickup_expectation)

# 计算每行的得分并写入文件
with open('../Gathered Data/Location_Ranking.txt', 'w') as file:
    for time_value, good_pickup_expectation, bad_pickup_expectation in zip(time_data, good_pickup_expectation,
                                                             bad_pickup_expectation):
        raw_score = 20
        #
        # # 根据 Bernoulli 分布模拟 pickup line 的好坏
        # is_good_pickup = bernoulli_dist.rvs()
        #
        # # 根据好坏 pickup line 的期望计算 binomial 分布的参数
        # if is_good_pickup:
        #     binom_p = p
        # else:
        #     binom_p = 1 - p

        # 如果好 pickup 的期望值不是 nan，加上好 pickup 的期望值
        if not np.isnan(good_pickup_expectation):
            raw_score += good_pickup_expectation

        # 如果坏 pickup 的期望值不是 nan，减去坏 pickup 的期望值
        if not np.isnan(bad_pickup_expectation):
            raw_score -= 2 * bad_pickup_expectation

        file.write(f"Score: {raw_score}\n")

print("Location rankings written to 'Location_Ranking.txt'.")

max_score = float('-inf')  # Initialize maximum score as negative infinity
line_number = 0  # Initialize line number
max_score_line = ""  # Initialize the line with the maximum score

with open('../Gathered Data/Location_Ranking.txt', 'r') as file:
    for i, line in enumerate(file, 1):  # Start line numbering from 1
        score = float(line.split(":")[1])  # Extract the score from the line

        # Update maximum score and corresponding line number if current score is greater
        if score > max_score:
            max_score = score
            line_number = i
            max_score_line = line.strip()  # Save the line with the maximum score

# Print the line with the maximum score and its line number
print("The line with the biggest score:", max_score_line)
print("Line number:", line_number)




