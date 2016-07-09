"""
Scraping module for soundfxcenter.
"""
import requests
from bs4 import BeautifulSoup


def pages(route):
    webpage = 'http://dota2.gamepedia.com'
    response = requests.get(webpage + route)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    heroes = soup.find_all('div', attrs={'style': 'position: relative;'})

    for hero in heroes:
        page = hero.find('a').attrs['href']
        name = hero.find('a').attrs['title'] + '_'
        yield name, webpage + page + '/Responses'


def sounds(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', attrs={'title': 'Play'})

    urls = [link.attrs['href'] for link in links]
    titles = [link.parent.text.strip(' Play ') for link in links]

    for url, title in zip(urls, titles):
        yield url, title
