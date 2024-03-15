locations = []
with open('../User Interface (Main)/Location_ranking_1.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 移除行尾的换行符并分割字符串以获取地点名称的前三个字符
        location_prefix = line.strip().split('. ')[1][:3]  # 只取前三个字符
        locations.append(location_prefix.lower())  # 转换为小写以保持一致性

# 第二步: 读取课程列表，解析每一行获取课程地点，并找到它的排名
ranks = []

# 打开并逐行读取文件
with open('../User Interface (Main)/sorted_courses_info.txt', 'r', encoding='utf-8') as file:
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

# 第三步和后续步骤不变



# 第三步: 将课程和它的排名写入新的txt文件
with open('../User Interface (Main)/ranked_courses.txt', 'w', encoding='utf-8') as file:
    for course_name, rank in ranks:
        file.write(f"{rank}\n")

print("Process complete, write into ranked_courses.txt")