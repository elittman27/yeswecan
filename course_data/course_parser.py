from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import glob
from preprocessor import TextPreprocessor

def clean_text(text):
    text = text.replace(u'\xa0', u' ').replace(u'聽', ' ').replace(u'鈥', '')
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

def parse_courses_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    courses = []
    for course_block in soup.find_all('div', class_='courseblock'):
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
    return courses_df


def generate_all_courses_csv():
    directory_path = r'course_data/department_htmls'

    if not os.path.exists(directory_path):
        print(f"Directory does not exist: {directory_path}")
        exit()

    print(f"Current working directory: {os.getcwd()}")

    file_paths = glob.glob(os.path.join(directory_path, '*'))

    if not file_paths:
        print("No files found in the directory.")
        exit()

    all_courses = pd.DataFrame()
    for path in file_paths:
        courses_df = parse_courses_from_html(path)
        all_courses = pd.concat([all_courses, courses_df], ignore_index=True)

    all_courses.to_csv('combined_courses.csv', index=False)

def generate_processed_csv(input_csv_path, output_csv_path):
    df = pd.read_csv(input_csv_path)
    df_preprocessed = df.copy()
    tp = TextPreprocessor()
    df_preprocessed['Course Title Preprocessed'] = df_preprocessed['Course Title'].apply(tp.preprocess)
    df_preprocessed['Description Preprocessed'] = df_preprocessed['Description'].apply(tp.preprocess)
    df_preprocessed.to_csv(output_csv_path, index=False)

generate_processed_csv('combined_courses.csv', 'combined_courses_preprocessed.csv')
generate_processed_csv('cs_courses.csv', 'cs_courses_preprocessed.csv')
