import numpy as np

def load_rankings(file_path):
    """从文本文件中加载排名数据"""
    with open(file_path, 'r') as file:
        rankings = np.array([int(line.strip()) for line in file.readlines()])
    return rankings

def assign_quantile_labels(rankings_1, rankings_2, n_quantiles=10):
    """根据分位数直接分配标签"""
    average_rank = np.mean([rankings_1, rankings_2], axis=0)
    quantiles = np.quantile(average_rank, np.linspace(0, 1, n_quantiles+1))
    labels = np.zeros_like(average_rank)
    for i in range(n_quantiles):
        labels[(average_rank > quantiles[i]) & (average_rank <= quantiles[i+1])] = i + 1
    return labels

# 加载排名数据
rankings_1 = load_rankings('../User Interface (Main)/Ranking_1.txt')
rankings_2 = load_rankings('../User Interface (Main)/ranked_courses.txt')

# 直接根据分位数分配档次标签
predicted_labels = assign_quantile_labels(rankings_1, rankings_2)
print(predicted_labels)

courses_info_path = '../User Interface (Main)/sorted_courses_info.txt'

def load_courses_info(file_path):
    with open(file_path, 'r') as file:
        courses = [line.split(',')[0].split(':')[0] for line in file.readlines()]  # 提取每行的第一项，去除符号
    return courses

courses = load_courses_info(courses_info_path)

# 使用之前计算得到的标签（predicted_labels），筛选出排名为高（标签为0）的课程
high_rank_courses = [courses[i] for i, label in enumerate(predicted_labels) if (label == 0 or label == 1)]

# 去除每个课程名称中的 "('" 字符
cleaned_high_rank_courses = [course.replace("('", "") for course in high_rank_courses]

print(cleaned_high_rank_courses)

