#utf-8
import requests
from bs4 import BeautifulSoup
import pandas as pd

def collect_user_rates(user_login):
    page_num = 1
    data = []
    while True:
        url = f'https://www.kinopoisk.ru/user/{user_login}/votes/'
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'lxml')
        entries = soup.find_all('div', class_='item')

        if len(entries) == 0:  #Признак остановки
            break
        for entry in entries:
            div_film_name = entry.find('div', class_='nameRus')
            film_name = div_film_name.find('a').text
            rating_div = entry.find('div', class_="vote")
            if rating_div is not None:
                rating = rating_div.text
            else:
                # Элемент не найден
                rating = "Элемент не найден"

            data.append({
                'film_name': film_name,
                'rating': rating
            })

        page_num += 1  # Переходим на следующую страницу
    return data

rates = collect_user_rates(input("Введите данные: "))
print(len(rates))

df = pd.DataFrame(rates)
df.to_excel('rates1.xlsx')

def get_rated_films(rates):
    rated_films = []
    while True:
        for item in rates:
            rating = float(item['rating'])  # Преобразуем строку в число с плавающей точкой
            if rating >= 8:
                rated_films.append(item)
        return rated_films

rates_ = get_rated_films(rates)
print(len(rates_))

df = pd.DataFrame(rates_)
df.to_excel('rates2.xlsx')