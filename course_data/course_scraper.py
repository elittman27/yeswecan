import requests
from bs4 import BeautifulSoup
import os

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def save_html(html, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html)

main_url = 'https://guide.berkeley.edu/courses/'

# Fetch and parse the main page HTML
main_page_html = fetch_html(main_url)
soup = BeautifulSoup(main_page_html, 'html.parser')

# Extract department URLs
department_links = soup.find_all('a', href=True)
department_urls = [link['href'] for link in department_links if link['href'].startswith('/courses/')]

# Directory to save department HTML files
os.makedirs('department_htmls', exist_ok=True)

# Scrape each department page
for url in department_urls:
    department_url = f'https://guide.berkeley.edu{url}'
    department_html = fetch_html(department_url)
    department_name = url.split('/')[-2]  # Assuming department name is in the URL
    filename = os.path.join('department_htmls', f"{department_name}.html")
    save_html(department_html, filename)
