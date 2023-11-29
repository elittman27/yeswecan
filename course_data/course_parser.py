from bs4 import BeautifulSoup
import pandas as pd

with open('cs_courses_html.txt', 'r', encoding='utf-8') as file:
    cs_courses_raw = file.read()
with open('ee_courses_html.txt', 'r', encoding='utf-8') as file:
    ee_courses_raw = file.read()



# Parse the HTML content
soup = BeautifulSoup(ee_courses_raw, 'html.parser')
courses = []
# Finding all course elements
courses_elements = soup.find_all('div', class_='courseblock')

courses_separated = []
for course_block in soup.find_all('div', class_='courseblock'):
    # Extracting course code, title, and units
    course_code = course_block.find('span', class_='code').get_text(strip=True)
    course_title = course_block.find('span', class_='title').get_text(strip=True)
    course_units = course_block.find('span', class_='hours').get_text(strip=True)

    desc_block = course_block.find('p', class_='courseblockdesc')
    if desc_block:
        terms_offered, description = desc_block.get_text(separator='|').split('|', 1)
    else:
        terms_offered, description = 'Not specified', 'Not specified'

    courses_separated.append({
        'Course Code': course_code,
        'Course Title': course_title,
        'Units': course_units,
        'Terms Offered': terms_offered.strip(),
        'Description': description.strip()
    })

# Converting the parsed data into a DataFrame
courses_html_separated_df = pd.DataFrame(courses_separated)
print(courses_html_separated_df.tail())
