from bs4 import BeautifulSoup
import requests

test_data = {'title': ''}

url = 'https://dtf.ru/'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
for link in soup.find_all('a', class_='content-link'):
    urls = requests.get(link.get('href'))
    data_parse = BeautifulSoup(urls.text, 'html.parser')
    for title in data_parse.find_all('h1', class_='content-title'):
        editorial = title.find('span', class_='content-title__editorial')
        if editorial:
            editorial.extract()
        cleaned_title = title.get_text().replace('\n', '').strip()
        test_data['title'] += cleaned_title + '!'
    for data in data_parse.find_all('div', class_='block-wrapper__content'):
        print(data)

