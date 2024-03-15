import requests
from bs4 import BeautifulSoup

# 目标网页URL
# url = 'https://explorecourses.stanford.edu/search?view=catalog&filter-coursestatus-Active=on&page=0&catalog=&academicYear=&q=cs+107e&collapse='
url = 'https://explorecourses.stanford.edu/search?view=catalog&filter-coursestatus-Active=on&page=0&catalog=&academicYear=&q=cs+107e&collapse='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Referer': 'https://www.example.com/',
    # 其他可能需要的头部
}

response = requests.get(url, headers=headers)


# 发送HTTP请求获取网页内容

# response = requests.get(url)
print(response.status_code)
# 确保请求成功
if response.status_code == 200:
    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    course_sections = soup.find_all('div', class_='searchResult')
    for section in course_sections:
        course_title_div = section.find('h2')
        if course_title_div and 'CS 107E:' in course_title_div.text:
            # Now that we've found the CS 107E section, look for the 2023-2024 Winter term
            winter_sections = section.find_all('div', class_='sectionContainer')
            for winter_section in winter_sections:
                term_heading = winter_section.find('h3', class_='sectionContainerTerm')
                if term_heading and '2023-2024 Winter' in term_heading.text:
                    # Extract the "Students enrolled" information
                    enrolled_info = winter_section.find(string=lambda text: 'Students enrolled:' in text)
                    if enrolled_info:
                        print(enrolled_info.strip())
                        break
else:
    print('Failed to retrieve the webpage')

