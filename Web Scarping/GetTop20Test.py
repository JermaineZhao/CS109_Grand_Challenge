def get_top_20_lines(input_file):
    with open(input_file, 'r') as file:
        # 读取每行的数值及其行号
        lines_with_values = [(i + 1, float(line.strip())) for i, line in enumerate(file) if
                             line.strip().isdigit() or line.strip().replace('.', '', 1).isdigit()]

        # 根据数值降序排序
        sorted_lines = sorted(lines_with_values, key=lambda x: x[1], reverse=True)

        # 获取前20大的行数
        top_20_lines = [line[0] for line in sorted_lines[:20]]

    return top_20_lines


# 示例文件路径，根据你的实际文件路径进行调整
input_file = '../User Interface (Main)/P(Class_i | Date).txt'

# 调用函数并打印结果
top_20_lines = get_top_20_lines(input_file)
print(f"前20大数值所在的行数：{top_20_lines}")
