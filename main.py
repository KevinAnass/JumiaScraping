import requests
from bs4 import BeautifulSoup
import pandas as pd

if __name__ == '__main__':
    url = input('Enter your jumia url like that : "https://www.jumia.ma/..../?page=" : ')
    columns = {'img url': [], 'name': [], 'price': [], 'discount': [], 'Reviews': [], 'Review /5': [], 'URL': []}
    r = requests.get(f'{url}1')
    soup = BeautifulSoup(r.content, "html.parser")
    pages = soup.find('div', {'class': 'pg-w -ptm -pbxl'}).find_all('a', href=True)
    lastPageCount = int(pages[-1]['href'].split('page=')[1].split('#')[0])
    if input('Extract tell end y=Yes/n=No : ') == 'n':
        lastPageUserWant = lastPageCount + 1
        while lastPageUserWant > lastPageCount:
            lastPageUserWant = int(input('Enter your last page Extract : '))
            if lastPageUserWant < lastPageCount:
                lastPageCount = lastPageUserWant
    for p in range(1, lastPageCount + 1):
        print(f'Extract Page : {p}')
        nextPage = requests.get(url + str(p))
        soup = BeautifulSoup(r.content, "html.parser")
        articles = soup.find('div', {'class': '-paxs row _no-g _4cl-3cm-shs'}).find_all('article',
                                                                                        {'class': 'prd _fb col c-prd'})
        for article in articles:
            columns['URL'].append(
                'https://www.jumia.ma' + article.find('a', href=True)['href'])
            columns['img url'].append(
                article.find('div', {'class': 'img-c'}).find('img', {'class': 'img'}).get('data-src'))
            columns['name'].append(article.find('div', {'class': 'info'}).find('h3', {'class': 'name'}).text)
            columns['price'].append(article.find('div', {'class': 'info'}).find('div', {'class': 'prc'}).text)
            discountDiv = article.find('div', {'class': 'info'}).find('div', {'class': 's-prc-w'})
            if discountDiv:
                columns['discount'].append(discountDiv.find('div', {'class': 'tag _dsct _sm'}).text)
            else:
                columns['discount'].append('none')
            review = article.find('div', {'class': 'info'}).find('div', {'class': 'rev'})
            if review:
                columns['Reviews'].append(review.text.split('(')[1].split(')')[0])
                columns['Review /5'].append(review.find('div', {'class': 'stars _s'}).text)
            else:
                columns['Reviews'].append('none')
                columns['Review /5'].append('none')
    data = pd.DataFrame(columns)
    data.to_excel('data.xlsx')
