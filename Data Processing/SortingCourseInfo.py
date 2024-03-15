# 假设您的txt文件名为'courses.txt'，排序后的文件名为'sorted_courses.txt'

def read_courses(file_path):
    courses = []
    with open(file_path, 'r') as file:
        for line in file:
            # 移除行尾的换行符并分割每一行为元组
            course_data = tuple(line.strip().strip("()").replace("'", "").split(', '))
            courses.append(course_data)
    return courses

def write_sorted_courses(courses, file_path):
    with open(file_path, 'w') as file:
        for course in courses:
            # 将元组转换回字符串格式，并写入文件
            line = f"('{course[0]}', '{course[1]}', '{course[2]}')\n"
            file.write(line)

# 读取课程信息
courses = read_courses('../Gathered Data/cs_courses_info.txt')

# 按照课程名称排序
sorted_courses = sorted(courses, key=lambda x: x[0])

# 将排序后的课程信息写入新的txt文件
write_sorted_courses(sorted_courses, '../User Interface (Main)/sorted_courses_info.txt')
