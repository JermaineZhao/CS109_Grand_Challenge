import requests
from bs4 import BeautifulSoup

# 初始化一个空列表来存储课程名称
courses_list = []

# 遍历第4页到第25页
for page in range(3, 25):
    # 构造URL。注意：这个URL模式基于示例，实际URL可能需要根据网站的具体结构调整
    url = f"https://explorecourses.stanford.edu/search?q=cs&view=catalog&filter-term-Winter=on&academicYear=&filter-term-Autumn=on&filter-term-Spring=on&page={page}&filter-coursestatus-Active=on&collapse="

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Referer': 'https://www.example.com/',
        # 其他可能需要的头部
    }

    # 发送HTTP GET请求
    response = requests.get(url,headers = headers)

    # 确认请求成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        courses = soup.find_all('div', class_='searchResult')
        for course in courses:
            # 对于每个课程，获取课程编号和标题
            course_number = course.find('span', class_='courseNumber').text.strip()
            course_title = course.find('span', class_='courseTitle').text.strip()
            # 检查课程编号是否以"CS"开头
            if course_number.startswith('CS'):
                # 将课程编号和标题添加到列表中
                courses_list.append(f"{course_number}: {course_title}")

# 写入到txt文档中
with open('../Gathered Data/cs_courses.txt', 'w', encoding='utf-8') as f:
    for course in courses_list:
        f.write(f"{course}\n")

print("完成写入!")
