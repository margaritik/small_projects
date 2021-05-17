import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = 'https://auto.ria.com/car/honda/'
# URL = 'https://browser-info.ru'
# Словарь с заголовками, чтобы сервер не заблокировал программу, имитируем работу браузера
# В консоль, раздел сеть CLTR + SHIFT + I
HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 YaBrowser/21.2.4.165 Yowser/2.5 Safari/537.36',
           'accept' : '*/*'}

def get_html(url, params = None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content_cars(html):
    soup = BeautifulSoup(html, 'html.parser')   #html url and document type to create the object
    soup = BeautifulSoup(html, 'lxml')

    items = soup.find_all('div', class_ = 'item ticket-title')
    def_data = soup.find_all('div', class_ = 'price-ticket')
    # print(len(items))
    results = []
    for (x, y) in zip(items, def_data):
        x_t = x.text
        results.append({
            'car': ' '.join(x_t.split()[1:-1]),
            'year': x_t.split()[-1],
            'price': y.find('span', class_='bold green size22').text
        })
    return results



def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')   #html url and document type to create the object
    soup = BeautifulSoup(html, 'lxml')

    # # print(soup)
    items = soup.find_all('div', class_ = 'item ticket-title')
    def_data = soup.find_all('div', class_ = 'price-ticket')
    # print(len(items), len(def_data))
    for (x, y) in zip(items, def_data):
        print(x.text, y.text)

def parse(url):
    html = get_html(url)   #parsing of the first page
    # print(html.status_code) #200 - достучались до страницы и получили контент
    if html.status_code == 200:
        res = get_content_cars(html.text)
    else:
        res = -1
        print('Error')
    return res




df_parsed = parse(URL)
df_parsed = pd.DataFrame(df_parsed)
for p in range(1, 15, 1):
    df = parse(URL+ '?page={}'.format(p))
    df = pd.DataFrame(df)
    df_parsed = pd.concat([df_parsed, df], axis = 0, ignore_index=True)
print(df_parsed)
