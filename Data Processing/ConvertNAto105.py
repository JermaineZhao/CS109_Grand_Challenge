# 指定您的文件路径
file_path = '../User Interface (Main)/Ranking_1.txt'

# 读取文件内容
with open(file_path, 'r') as file:
    lines = file.readlines()

# 替换NA为105
with open(file_path, 'w') as file:
    for line in lines:
        file.write(line.replace('NA', '105'))
