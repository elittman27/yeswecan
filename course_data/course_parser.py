from bs4 import BeautifulSoup
import pandas as pd
import re

def clean_text(text):
    # Replace non-breaking spaces and other special characters
    text = text.replace(u'\xa0', u' ').replace(u'聽', ' ').replace(u'鈥', '')
    # Further cleaning with regular expressions if necessary
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    return text.strip()

def parse_courses_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    courses = []
    for course_block in soup.find_all('div', class_='courseblock'):
        # Extracting course code, title, and units
        course_code = course_block.find('span', class_='code').get_text(strip=True)
        course_title = course_block.find('span', class_='title').get_text(strip=True)
        course_units = course_block.find('span', class_='hours').get_text(strip=True)

        desc_block = course_block.find('p', class_='courseblockdesc')
        if desc_block:
            terms_offered, description = desc_block.get_text(separator='|').split('|', 1)
            terms_offered = terms_offered.strip()  # Trim spaces
            description = description.strip().split('|')[0].strip()  # Trim spaces and remove text after "|"
        else:
            terms_offered, description = 'Not specified', 'Not specified'

        course_code = clean_text(course_code)
        course_title = clean_text(course_title)
        course_units = clean_text(course_units)
        terms_offered = clean_text(terms_offered)
        description = clean_text(description)
        
        courses.append({
            'Course Code': course_code,
            'Course Title': course_title,
            'Units': course_units,
            'Terms Offered': terms_offered.strip(),
            'Description': description.strip()
        })
    courses_df = pd.DataFrame(courses)
    print(courses_df.head())
    return courses_df


file_paths = ['course_data\cs_courses_html.txt', 
              'course_data\ee_courses_html.txt']

# Parsing and combining course data from all files
all_courses = pd.DataFrame()
for path in file_paths:
    courses_df = parse_courses_from_html(path)
    all_courses = pd.concat([all_courses, courses_df], ignore_index=True)

# Export to CSV
all_courses.to_csv('combined_courses.csv', index=False)