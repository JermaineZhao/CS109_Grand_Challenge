def get_integer_input(prompt, valid_range):
    """Asks the user for an integer input within a valid range. Re-prompts if the input is invalid."""
    while True:
        user_input = input(prompt)
        try:
            # Attempt to convert the input to an integer
            user_input_int = int(user_input)
            if user_input_int in valid_range:
                return user_input_int
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            try:
                # Attempt to convert to float and then to int, if necessary
                user_input_float = float(user_input)
                user_input_int = int(user_input_float)
                if user_input_int in valid_range:
                    print("Note: Decimal values are rounded down.")
                    return user_input_int
                else:
                    print("Invalid input. Please try again.")
            except ValueError:
                print("Please enter a valid integer.")

def get_cs_course_input(prompt):
    """Asks the user for a CS course name, ensures it starts with 'CS', and formats it to 'CS [Number]'. Re-prompts if the input is invalid."""
    while True:
        course_input = input(prompt).strip()  # Remove leading/trailing whitespace
        if not course_input.upper().startswith('CS'):
            print("The course name must start with 'CS'. Please try again.")
        else:
            # Extract the part after 'CS' and remove any spaces
            course_number = ''.join(filter(str.isalnum, course_input[2:])).upper()
            if not course_number:
                print("Please enter a valid course number.")
            else:
                # Format and return the course name in standard format
                return f"CS {course_number}"



# Initialize an empty dictionary to store answers
user_answers = {}

# Question 1: User's name
user_answers['name'] = input("What’s your name? ")

# Question 2: User's grade, with input validation
grade_prompt = "Which grade are you in? (1 for freshman, 2 for sophomore, 3 for junior, 4 for senior, 5 for Coterm, 6 for Master, 7 for PhD, 8 for SCPD) "
user_answers['grade'] = get_integer_input(grade_prompt, range(1, 9))
if user_answers['grade'] == 8:
    print("Sorry, there’s not enough information for SCPD right now!")

# Question 3: Number of CS classes
num_cs_classes = int(input("How many CS classes are you gonna take next quarter? "))
user_answers['cs_classes_count'] = num_cs_classes

# Questions based on the number of CS classes
user_answers['cs_classes'] = []
for i in range(1, num_cs_classes + 1):
    class_name = get_cs_course_input(f"What is the {i}th CS class you will take? ")
    user_answers['cs_classes'].append(class_name)


# Question 4: Sexual orientation, with input validation
orientation_prompt = "What is your sexual orientation? (1 for 'I love male', 2 for 'I love female') "
user_answers['sexual_orientation'] = get_integer_input(orientation_prompt, [1, 2])

# Remaining questions
user_answers['crushes'] = int(input("How many crushes will you meet on average in 100 people of your sexual orientation? "))
user_answers['pickup_lines'] = int(input("How many pickup lines can you usually come up with in 10 minutes? "))
user_answers['valid_pickup_lines'] = int(input("Among these pickup lines, how many are good (valid) pickup lines? "))

# adjust for gender
if user_answers['sexual_orientation'] == 1:
    user_answers['crushes'] *= 0.655
elif user_answers['sexual_orientation'] == 2:
    user_answers['crushes'] *= 0.344

# Assuming the code runs in an interactive environment, this would capture and store user responses.


# Calculating for P(Date)
import numpy as np
from scipy.optimize import minimize
from scipy.stats import t

# Adjustable variable
target_probs = np.array([3 / 300, 13 / 300, 3 / 300])
x_values = np.array([5, 15, 25])

# 综合函数：计算特定周小时数下的可能遇到的crush数量的概率
def calculate_probability(weekly_hour, crush_100):
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

def process_file_Pdate(input_file, output_file, crush_100):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            parts = line.strip().split(',')
            # 检查是否存在第二项且第二项不是 "None"
            if len(parts) > 1 and parts[1].strip() != "None":
                weekly_hour = float(parts[1].strip())
                probability = calculate_probability(weekly_hour, crush_100)
                outfile.write(f"{probability}\n")
            else:
                outfile.write("NA\n")

# 请根据你的文件路径和需要的crush_100的值调整下面的变量
input_file = 'FINAL_Course_Info.txt'
output_file = 'P_Date_All.txt'
crush_100 = user_answers['crushes']

process_file_Pdate(input_file, output_file, crush_100)

print(f"P(Date) Process Complete, saved as {output_file}")


# Calculate P(Class_i | Year_j)

# First, Calculate (Class_i, Year_j), the number of students who is Class_i & Year_j
def calculate_students_per_course(size_file, distribution_file, output_file):
    with open(size_file, 'r') as size_f, open(distribution_file, 'r') as dist_f, open(output_file, 'w') as out_f:
        for size_line, dist_line in zip(size_f, dist_f):
            if 'None' in size_line or 'Information not found' in size_line or 'None' in dist_line or 'Information not found' in dist_line:
                out_f.write('NA\n')
                continue

            # 提取课程大小，确保去除了多余的引号
            _, size_str, _ = size_line.strip().split(',', 2)
            size = size_str.strip().strip("'\"")  # 去除可能的单引号和双引号

            # 提取年级分布比例
            _, _, distribution = dist_line.partition(':')
            ratios = [float(ratio.strip()) for ratio in distribution.split(',')[1:8]]  # 从第三项开始提取比例，跳过课程名和时间

            # 修正：确保我们基于正确的课程大小和分布比例计算每个年级的学生数
            try:
                class_size = float(size)
                students_per_year = [round(class_size * (ratio/100)) for ratio in ratios]
                out_f.write(','.join(map(str, students_per_year)) + '\n')
            except ValueError as e:
                out_f.write('NA\n')

size_file = 'sorted_courses_info.txt'
distribution_file = 'FINAL_Course_Info.txt'
output_file = '(Class_i, Year_j).txt'

calculate_students_per_course(size_file, distribution_file, output_file)
print(f"(Class_i, Year_j) Process Complete, saved as {output_file}")

# Calculate P(Class_i | Year_j)
frosh = 1705
sophomore= 1736
junior = 2138
senior = 2042
coterm = 300
master = 2103
phD = 799

Total_students = [frosh, sophomore, junior, senior, coterm, master, phD]

def process_data(input_file, output_file, total_students):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            values = line.strip().split(',')  # 假设每项由逗号分隔
            processed_values = []

            for i, value in enumerate(values):
                try:
                    # 将每一项除以对应的Total_students值
                    processed_value = float(value) / total_students[i]
                except ValueError:
                    # 如果转换失败（例如，空白行或非数字字符串），则将值保留为原样
                    processed_value = value
                except IndexError:
                    # 如果行中的项数多于Total_students列表中的元素数，跳过多余的项
                    break

                processed_values.append(str(processed_value))

            # 将处理后的值写入到新文件，使用逗号分隔
            outfile.write(','.join(processed_values) + '\n')

# 示例变量和调用函数
input_file = '(Class_i, Year_j).txt'
output_file = 'P(Class_i | Year_j).txt'

process_data(input_file, output_file, Total_students)

print(f"P(Class_i | Year_j) Process Complete, saved as {output_file}")

# Here is the 7*7 matrix of P(Year_j | Date), derivation in file "Truncated Normal Distrubution.py"
array_P_YD = [
    [0.28632566524581116, 0.2513997564368522, 0.1938085507876501, 0.1311844618391977, 0.0779632757613583, 0.04068101630795232, 0.018637273621178178],
    [0.22586438996957647, 0.2258643899695764, 0.1983135272814682, 0.15288343102934834, 0.10348320825993798, 0.06150034683321728, 0.03209070665687543],
    [0.16549385679670028, 0.1884852209604773, 0.18848522096047723, 0.16549385679670037, 0.12758216238798917, 0.08635737301130468, 0.051322417241453415],
    [0.11589925439111354, 0.15033931272239498, 0.17122531993641898, 0.1712253199364189, 0.15033931272239504, 0.11589925439111354, 0.07844948663550579],
    [0.07602970831624403, 0.11232433612176577, 0.1457020891399309, 0.16594386642205924, 0.1659438664220592, 0.14570208913993096, 0.11232433612176577],
    [0.04662273926463917, 0.07844948663550583, 0.11589925439111355, 0.150339312722395, 0.171225319936419, 0.17122531993641893, 0.15033931272239506],
    [0.026779891844897652, 0.05132241724145334, 0.08635737301130472, 0.12758216238798917, 0.16549385679670028, 0.1884852209604773, 0.18848522096047723]
]

matrix_P_YD = np.array(array_P_YD)


# Calculate P(Class_i | Date)
def multiply_sum_and_write(input_file, output_file, matrix, a):
    # 确保a的值在正确的范围内
    if a < 1 or a > 7:
        print("a的值应该在1到7之间")
        return

    # 选择矩阵的第a行
    matrix_row = matrix[a - 1]

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.strip() == "NA":
                outfile.write("NA\n")
                continue

            # 分割每行的值并转换为浮点数
            try:
                values = [float(value) for value in line.strip().split(',')]
            except ValueError:
                outfile.write("NA\n")  # 如果转换失败，则写入NA
                continue

            # 计算乘积
            multiplied_values = np.multiply(matrix_row, values)

            # 将乘积的总和写入到新文件
            total_sum = sum(multiplied_values)
            outfile.write(f"{total_sum}\n")

input_txt = 'User Interface (Main)/P(Class_i | Year_j).txt'  # 你的输入文件名
output_txt = 'User Interface (Main)/P(Class_i | Date).txt'  # 输出文件名
a =  user_answers['grade']

# 调用函数
multiply_sum_and_write(input_txt, output_txt, matrix_P_YD, a)

print(f"P(Class_i | Date) Process Complete, saved as {output_file}")

# Sorting P(Class_i | Date)
def sort_values_and_write_order(input_file, output_file):
    values = []
    nas = []

    # 读取输入文件
    with open(input_file, 'r') as file:
        for line_number, line in enumerate(file):
            value = line.strip()
            if value == "NA":
                nas.append((line_number, "NA"))
            else:
                values.append((line_number, float(value)))

    # 按值排序，保留原始行号
    sorted_values = sorted(values, key=lambda x: x[1], reverse=True)

    # 创建一个与原始文件同样长度的列表，用于存放排序后的位置
    order = [""] * (len(values) + len(nas))

    # 填充排序后的位置
    for order_num, (line_number, _) in enumerate(sorted_values, start=1):
        order[line_number] = str(order_num)

    # 处理NA值
    for line_number, _ in nas:
        order[line_number] = "NA"

    # 写入新文件
    with open(output_file, 'w') as file:
        for line_order in order:
            file.write(f"{line_order}\n")


# 示例文件路径，根据你的实际文件路径进行调整
input_file = 'P(Class_i | Date).txt'
output_file = 'Ranking_1.txt'

# 调用函数
sort_values_and_write_order(input_file, output_file)

print(f"Ranking 1 Process Complete, saved as {output_file}")




# Get the ranking by location
pickup_user = user_answers['pickup_lines']
good_pickup_user = user_answers['valid_pickup_lines']

with open('Machine_learned_Walktime.txt', 'r') as file:
    time_data = [float(line.strip()) for line in file]

lambda_parameter = []

for i in range(len(time_data)):
    lambda_parameter.append(pickup_user * time_data[i] / 10)


poisson_expectation = lambda_parameter

from scipy.stats import bernoulli, binom

p = 0
# 模拟好坏 pickup line
if pickup_user != 0:
    p = good_pickup_user / pickup_user
bernoulli_dist = bernoulli(p)

# adjustable variable
bonus = 1
penalty = -1.2

# 计算新的数组
adjusted_good_pickup_expectation = []
adjusted_bad_pickup_expectation = []

for expectation in poisson_expectation:
    # 生成伯努利随机数决定当前情境是好是坏的pickup line
    if bernoulli_dist.rvs() == 1:  # 如果是好的pickup line
        adjusted_good_pickup_expectation.append(expectation)
        adjusted_bad_pickup_expectation.append(0)
    else:  # 如果是坏的pickup line
        adjusted_good_pickup_expectation.append(0)
        adjusted_bad_pickup_expectation.append(expectation)

# 使用调整后的期望值计算新数组
new_array = [20 + bonus * good + penalty * bad for good, bad in zip(adjusted_good_pickup_expectation, adjusted_bad_pickup_expectation)]

# 写入到txt文件中
output_file_path = 'User Interface (Main)/Location_Ranking.txt'  # 调整为你的文件路径
with open(output_file_path, 'w') as file:
    for value in new_array:
        file.write(f"{value}\n")

print(f"Location_Ranking Process Complete, saved as {output_file_path}")



# Get the location's ranking
location_file_path = 'unique_locations_full_names.txt'
ranking_file_path = 'User Interface (Main)/Location_Ranking.txt'

# Load the locations
with open(location_file_path, 'r') as file:
    locations = file.read().splitlines()

# Load the scores
with open(ranking_file_path, 'r') as file:
    scores = file.read().splitlines()

# Convert scores to float for sorting
scores = [float(score) for score in scores]

# Map each location to its score
location_scores = dict(zip(locations, scores))

# Sort the locations by score in descending order
sorted_locations = sorted(location_scores.items(), key=lambda x: x[1], reverse=True)

# Prepare the ranked list with only the locations, not including the scores this time.
ranked_list_simple = [f"{rank+1}. {location[0]}" for rank, location in enumerate(sorted_locations)]

# Path for the simplified ranked file
ranked_file_path_simple = 'Location_ranking_1.txt'

with open(ranked_file_path_simple, 'w') as file:
    for item in ranked_list_simple:
        file.write(f"{item}\n")


print(f"Location_Ranking_1 Process Complete, saved as {ranked_file_path_simple}")

# Get the location ranking
locations = []
with open('Location_ranking_1.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 移除行尾的换行符并分割字符串以获取地点名称的前三个字符
        location_prefix = line.strip().split('. ')[1][:3]  # 只取前三个字符
        locations.append(location_prefix.lower())  # 转换为小写以保持一致性

# 第二步: 读取课程列表，解析每一行获取课程地点，并找到它的排名
ranks = []

# 打开并逐行读取文件
with open('sorted_courses_info.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 假设每一行的格式确实为 "('课程名:', '排名', '地点')"
        # 移除两侧的括号和空格，然后以逗号和空格分割
        parts = line.strip("()\n ").split("', '")
        if len(parts) == 3:
            course_name, _, location_name = parts
            # 提取地点名称的前三个字符，并转换为小写
            location_prefix = location_name[:3].lower()
            if location_prefix.startswith("60"):
                location_prefix = "60"
            # 尝试找到这个前缀对应的排名
            try:
                rank = locations.index(location_prefix) + 1
                ranks.append((course_name, rank))
            except ValueError:
                print(f"error\n{line}")
                # 如果找不到地点，跳过这一行
                continue

# 第三步: 将课程和它的排名写入新的txt文件
with open('ranked_courses.txt', 'w', encoding='utf-8') as file:
    for course_name, rank in ranks:
        file.write(f"{rank}\n")

print("Process complete, write into ranked_courses.txt")

# process ranked_courses.txt to make ranking in scale of 1-210
# 读取上传的文件内容
file_path = 'ranked_courses.txt'

# 读取文件内容
with open(file_path, 'r') as file:
    course_ranks = [int(line.strip()) for line in file.readlines()]

# 排序并重新排名
sorted_ranks = sorted(course_ranks, reverse=True)  # 从大到小排序
new_ranks = {}
current_rank = 1

for i, rank in enumerate(sorted_ranks):
    if rank not in new_ranks:
        new_ranks[rank] = current_rank
        current_rank += sorted_ranks.count(rank)  # 计算下一个排名

# 生成新的排名列表，保持原列表的顺序
re_ranked_courses = [new_ranks[rank] for rank in course_ranks]

# 将重新排名的结果写回原文件
with open(file_path, 'w') as file:
    for rank in re_ranked_courses:
        file.write(f"{rank}\n")





# Convert the NA to mean = 105
file_path = 'Ranking_1.txt'

# 读取文件内容
with open(file_path, 'r') as file:
    lines = file.readlines()

# 替换NA为105
with open(file_path, 'w') as file:
    for line in lines:
        file.write(line.replace('NA', '105'))
#
#
# from sklearn.naive_bayes import GaussianNB
# import numpy as np
#
# def load_rankings(file_path):
#     """从文本文件中加载排名数据"""
#     with open(file_path, 'r') as file:
#         rankings = np.array([int(line.strip()) for line in file.readlines()])
#     return rankings
#
# def compute_features_labels(rankings_1, rankings_2, n_labels=10):
#     """计算特征和标签，将数据分为n_labels个档次"""
#     features = np.vstack((rankings_1, rankings_2)).T
#     average_rank = np.mean([rankings_1, rankings_2], axis=0)
#     quantiles = np.quantile(average_rank, np.linspace(0, 1, n_labels+1)[1:-1])
#     labels = np.zeros_like(average_rank)
#     for i, q in enumerate(quantiles, start=1):
#         labels[average_rank <= q] = i-1
#     labels[average_rank > quantiles[-1]] = n_labels-1
#     return features, labels
#
# def train_and_predict(features, labels):
#     """训练模型并进行预测"""
#     model = GaussianNB()
#     model.fit(features, labels)
#     predicted_labels = model.predict(features)
#     return predicted_labels
#
# # 加载排名数据
# rankings_1 = load_rankings('Ranking_1.txt')
# rankings_2 = load_rankings('ranked_courses.txt')
#
# # 计算特征和标签，分为10个档次
# features, labels = compute_features_labels(rankings_1, rankings_2, 10)
#
# # 训练模型并进行预测
# predicted_labels = train_and_predict(features, labels)
#
# # 输出预测的档次
# print(predicted_labels)

import numpy as np

def load_rankings(file_path):
    """从文本文件中加载排名数据"""
    with open(file_path, 'r') as file:
        rankings = np.array([int(line.strip()) for line in file.readlines()])
    return rankings

# adjustable variable
w1 = 0.55  # 为rankings_1设置的权重
w2 = 0.45  # 为rankings_2设置的权重

def assign_quantile_labels(rankings_1, rankings_2, n_quantiles=15):
    """根据分位数直接分配标签"""
    average_rank = (w1 * rankings_1 + w2 * rankings_2) / (w1 + w2)
    quantiles = np.quantile(average_rank, np.linspace(0, 1, n_quantiles+1))
    labels = np.zeros_like(average_rank)
    for i in range(n_quantiles):
        labels[(average_rank > quantiles[i]) & (average_rank <= quantiles[i+1])] = i + 1
    return labels

# 加载排名数据
rankings_1 = load_rankings('Ranking_1.txt')
rankings_2 = load_rankings('ranked_courses.txt')

# 直接根据分位数分配档次标签
predicted_labels = assign_quantile_labels(rankings_1, rankings_2)

# 检查每个档次中的课程数量
# np.bincount(predicted_labels.astype(int))


courses_info_path = 'sorted_courses_info.txt'

def load_courses_info(file_path):
    with open(file_path, 'r') as file:
        courses = [line.split(',')[0].split(':')[0] for line in file.readlines()]  # 提取每行的第一项，去除符号
    return courses

courses = load_courses_info(courses_info_path)

# 使用之前计算得到的标签（predicted_labels），筛选出排名为高（标签为0）的课程
high_rank_courses = [courses[i] for i, label in enumerate(predicted_labels) if (label == 0 or label == 1 )]
m_high_rank_courses = [courses[i] for i, label in enumerate(predicted_labels) if (label == 2 or label == 3 or label == 4 or label == 5)]
medium_rank_courses = [courses[i] for i, label in enumerate(predicted_labels) if (label == 9 or label == 6 or label == 7 or label == 8)]
m_low_rank_courses = [courses[i] for i, label in enumerate(predicted_labels) if (label == 11 or label == 12 or label == 10)]
low_rank_courses = [courses[i] for i, label in enumerate(predicted_labels) if (label == 13 or label == 14)]


# 去除每个课程名称中的 "('" 字符
cleaned_high_rank_courses = [course.replace("('", "") for course in high_rank_courses]

# print(cleaned_high_rank_courses)


# Generate Report
name = user_answers['name']
file_path = f"CS109GrandChallenge/CS_Love_Report_for_{name}.txt"
user_classes = user_answers['cs_classes']  # user_answers['cs_classes']

with open(file_path, 'w') as file:
    file.write(f"Hi, {name}!\n\n")

with open(file_path, 'a') as file:
    file.write("Welcome to Stanford CS Love!\n\n"
           "Based on your personal preferences and the dynamics of Stanford CS Classes, we've crafted this unique CS Love Report just for you.\n\n"
               "The CS courses you'll be taking next semester are:  \n")

with open(file_path, 'a') as file:
    for user_class in user_classes:
        user_class = "('" + user_class
        prob = "NA"
        if user_class in high_rank_courses:
            prob = "HIGH"
        elif user_class in m_high_rank_courses:
            prob = "MEDIUM_HIGH"
        elif user_class in medium_rank_courses:
            prob = "MEDIUM"
        elif user_class in m_low_rank_courses:
            prob = "MEDIUM_LOW"
        elif user_class in low_rank_courses:
            prob = "LOW"

        user_class = user_class[2:]
        file.write(f"{user_class}, which has '{prob}' probability of finding a love; \n")
    file.write("\n\nBased on your data, here are the courses that are most likely to help you find a partner:\n")
    for high_class in high_rank_courses:
        high_class = high_class[2:]
        file.write(f"{high_class}\n")

    file.write("\nBased on your data, here are the courses that are least likely to help you find a partner:\n")
    for low_class in low_rank_courses:
        low_class = low_class[2:]
        file.write(f"{low_class}\n")

    file.write("\nMay your college days be full of joy and serendipitous encounters. 😉!")

print(f"\n\n Hi, {name}! Your CS Love Report is generated. You can find it in {file_path}. Thanks!")




