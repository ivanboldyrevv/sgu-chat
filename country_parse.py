from bs4 import BeautifulSoup
import requests
import sqlite3


con = sqlite3.connect('instance/database.db')
cursor = con.cursor()

url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2'
page = requests.get(url)


soup = BeautifulSoup(page.text, 'html.parser')

countries = []
final_countries = []

for country in soup.find_all('tr'):
    text = country.text
    countries.append(text.split())

for i in countries:
    if i[0] == 'Номер':
        continue
    else:
        final_countries.append(i)

for i in final_countries:
    cursor.execute('INSERT INTO countries (name) VALUES (?)', (i[1],))
    con.commit()


