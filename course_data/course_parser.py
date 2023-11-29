from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import glob

# HOW TO USE:
# 1. Go to https://guide.berkeley.edu/courses/
# 2. Select the department you want to parse
# 3. Copy HTML
# 4. Paste HTML into a text file and save it in the raw_data folder
# 5. Run the script


def clean_text(text):
    text = text.replace(u'\xa0', u' ').replace(u'聽', ' ').replace(u'鈥', '')
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
            terms_offered = terms_offered.strip()
            description = description.strip().split('|')[0].strip()
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

# Specify the directory containing your files
directory_path = r'course_data/raw_data'  # Use a raw string literal and forward slashes

# Check if the directory exists
if not os.path.exists(directory_path):
    print(f"Directory does not exist: {directory_path}")
    exit()

# Print the current working directory for debugging
print(f"Current working directory: {os.getcwd()}")

# Use glob to find all files in the directory
file_paths = glob.glob(os.path.join(directory_path, '*'))

# Check if file_paths is empty
if not file_paths:
    print("No files found in the directory.")
    exit()

# Parsing and combining course data from all files
all_courses = pd.DataFrame()
for path in file_paths:
    courses_df = parse_courses_from_html(path)
    all_courses = pd.concat([all_courses, courses_df], ignore_index=True)

# Export to CSV
all_courses.to_csv('combined_courses.csv', index=False)