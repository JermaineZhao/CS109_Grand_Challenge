import requests
from bs4 import BeautifulSoup
import re

# url = 'https://explorecourses.stanford.edu/search?view=catalog&filter-coursestatus-Active=on&page=0&catalog=&academicYear=&q=cs+107e&collapse='
# url = 'https://explorecourses.stanford.edu/search?q=cs&view=catalog&filter-term-Winter=on&academicYear=&filter-term-Autumn=on&filter-term-Spring=on&page=3&filter-coursestatus-Active=on&collapse='


# url = 'https://explorecourses.stanford.edu/search?q=cs&view=catalog&academicYear=&filter-term-Autumn=on&page=2&filter-coursestatus-Active=on&collapse='

results = []
for page in range(1, 12):#should be 12
    # 构造URL。注意：这个URL模式基于示例，实际URL可能需要根据网站的具体结构调整
    url = f'https://explorecourses.stanford.edu/search?q=cs&view=catalog&academicYear=20222023&filter-term-Spring=on&page={page}&filter-coursestatus-Active=on&collapse='

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Referer': 'https://www.example.com/',
        # 其他可能需要的头部
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Iterate over each courseInfo section
    for course_info in soup.find_all('div', class_='courseInfo'):
        # Extract the course number
        course_number = course_info.find('span', class_='courseNumber').text.strip()
        if course_number.startswith('CS'):

            # Find the section details where enrollment info is contained
            # section_details = course_info.find('div', id=lambda x: x and x.startswith('schedule_'))
            section_details = course_info.find('li', class_='sectionDetails')
            if section_details:


                enrolled_text = section_details.find(string=re.compile('Students enrolled:'))
                if enrolled_text:



                    match = re.search(r"Students enrolled:\s*(\d+)", enrolled_text)
                    if match:
                        students_enrolled = match.group(1)
                        enrolled_info = f"{students_enrolled}"
                    else:
                        enrolled_info = "Information not found"
                else:
                    enrolled_info = "Information not found"

                # Extract class location
                location_links = section_details.find_all('a',
                                                          href=lambda
                                                              x: x and 'http://campus-map.stanford.edu/?srch=' in x)
                if location_links:
                    # Assuming you only need the first matching link
                    location_link = location_links[0]
                    location_href = location_link['href']
                    # Extract just the room number from the href or the link text, based on your requirements
                    location = location_link.text.strip()
                else:
                    location = "Location not found"

            else:
                enrolled_info = "Enrollment info not found"
                location = "Location not found"

            # Append the extracted info to the results list

            new_data = (course_number, enrolled_info, location)
            results.append(new_data)

for page in range(1, 19):#should be 12
    # 构造URL。注意：这个URL模式基于示例，实际URL可能需要根据网站的具体结构调整
    url = f"https://explorecourses.stanford.edu/search?q=cs&view=catalog&page={page}&academicYear=20232024&filter-term-Autumn=on&filter-term-Winter=on&collapse=&filter-coursestatus-Active=on"


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    response = requests.get(url, headers=headers)


    soup = BeautifulSoup(response.content, 'html.parser')




    # Iterate over each courseInfo section
    for course_info in soup.find_all('div', class_='courseInfo'):
        # Extract the course number
        course_number = course_info.find('span', class_='courseNumber').text.strip()
        if course_number.startswith('CS'):

            # Find the section details where enrollment info is contained
            # section_details = course_info.find('div', id=lambda x: x and x.startswith('schedule_'))
            section_details = course_info.find('li',class_ = 'sectionDetails')
            if section_details:
                # Extract students enrolled
                # enrolled_text = section_details.find(string=lambda x: 'Students enrolled:' in x)
                enrolled_text = section_details.find(string=re.compile('Students enrolled:'))
                if enrolled_text:

                    match = re.search(r"Students enrolled:\s*(\d+)", enrolled_text)
                    if match:
                        students_enrolled = match.group(1)
                        enrolled_info = f"{students_enrolled}"
                    else:
                        enrolled_info = "Information not found"
                else:
                    enrolled_info = "Information not found"



                # Extract class location
                location_links = section_details.find_all('a',
                                                          href=lambda x: x and 'http://campus-map.stanford.edu/?srch=' in x)
                if location_links:
                    # Assuming you only need the first matching link
                    location_link = location_links[0]
                    location_href = location_link['href']
                    # Extract just the room number from the href or the link text, based on your requirements
                    location = location_link.text.strip()
                else:
                    location = "Location not found"

            else:
                enrolled_info = "Enrollment info not found"
                location = "Location not found"

            # Append the extracted info to the results list


            new_data = (course_number, enrolled_info, location)
            # results.append(new_data)
            for i, (course_number, enrolled_info, location) in enumerate(results):
                if course_number == new_data[0]:
                    # 如果存在，更新这条记录
                    results[i] = new_data
                    print("hahahah")

                    break
            else:
                # 如果不存在，添加新记录
                results.append(new_data)


with open('../Gathered Data/cs_courses_info.txt', 'w', encoding='utf-8') as f:
    for course in results:
        f.write(f"{course}\n")
# Print results
for course_number, enrolled_info, location in results:
    print(f"Class Number: {course_number}, Students enrolled: {enrolled_info}, Location: {location}")