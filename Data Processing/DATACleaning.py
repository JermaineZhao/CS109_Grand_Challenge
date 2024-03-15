# def extract_after_colon(input_file, output_file):
#     with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
#         for line in infile:
#             # 分割每行在第一个冒号处，并保留冒号后面的部分
#             parts = line.split(':', 1)
#             if len(parts) > 1:
#                 outfile.write(parts[1].strip() + '\n')
#
# # 调用函数
# input_file = '文本111.txt'  # 更改为你的输入文件名
# output_file = '文本111_new.txt'  # 输出文件名，可以按需更改
# extract_after_colon(input_file, output_file)

# 假设你的文件名为 'input.txt'，并将输出写入 'output.txt'
#
# def check_lines(filename):
#     invalid_lines = []  # 存储项数不足9的行的行数
#     with open(filename, 'r') as file:
#         for line_number, line in enumerate(file, start=1):
#             items = line.strip().split(',')  # 删除可能的前后空格，并按逗号分割
#             if len(items) != 9:  # 检查是否有10项（包括第一个数字）
#                 invalid_lines.append(line_number)
#
#     return invalid_lines
#
#
# # 调用函数并打印结果
# filename = '文本111_new.txt'  # 你的输入文件路径
# invalid_lines = check_lines(filename)
# print(f"行数不足9项的行有：{invalid_lines}")
#
# # # 如果你需要将这些行数写入一个文件
# # with open('output.txt', 'w') as out_file:
# #     for line_number in invalid_lines:
# #         out_file.write(f"{line_number}\n")
#
# def process_file(input_filename, output_filename):
#     with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
#         for line in infile:
#             items = line.strip().split(',')
#             if len(items) < 9:  # 检查项数是否少于9
#                 outfile.write("None\n")
#             else:
#                 outfile.write(line)  # 如果行的项数足够，保持原样写入
#
# # 请根据你的文件路径修改这些文件名
# input_filename = '文本111_new.txt'
# output_filename = '111_new_new.txt'
#
# process_file(input_filename, output_filename)
#
# print(f"处理完成，输出文件已保存为 {output_filename}")

def add_prefix_to_file(prefix_file, target_file, output_file):
    # 读取前缀文件，并提取每行的第一项作为前缀
    with open(prefix_file, 'r') as pf:
        prefixes = [line.split(',')[0].strip("('") for line in pf.readlines()[:210]]

    # 读取目标文件，并为指定的行添加前缀
    with open(target_file, 'r') as tf, open(output_file, 'w') as of:
        for i, line in enumerate(tf, start=1):
            if 2 <= i <= 211:  # 为第2到211行添加前缀
                of.write(f"{prefixes[i-2]} {line}")
            else:
                of.write(line)


# 调用函数
prefix_filename = '../User Interface (Main)/sorted_courses_info.txt'  # 包含前缀的文件名
target_filename = '../Gathered Data/111_new_new.txt'  # 目标文件名
output_filename = '../User Interface (Main)/FINAL_Course_Info.txt'  # 输出文件名

add_prefix_to_file(prefix_filename, target_filename, output_filename)

print(f"处理完成，带前缀的内容已保存到 {output_filename}")


# def remove_prefix_from_file(input_filename, output_filename):
#     with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
#         for line in infile:
#             # 去除每行开头的 "('"
#             if line.startswith("('"):
#                 line = line[2:]  # 从第三个字符开始截取到行尾
#             outfile.write(line)
#
# # 调用函数
# input_filename = '111_damn_new.txt'  # 你的原始文件名
# output_filename = 'FINAL_Course_Info.txt'  # 清理后的输出文件名
#
# remove_prefix_from_file(input_filename, output_filename)
#
# print(f"处理完成，修改后的文件已保 {output_filename}")
