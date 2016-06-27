"""
Scraping module for myinstants.
"""
import requests
from bs4 import BeautifulSoup


def pages(route):
    webpage = 'https://www.myinstants.com'
    response = requests.get(webpage + route)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    for page in range(1, int(soup.select('ul[class="pagination"]')
                      [0].contents[2].strip("\n").split(" ")[2])):
        yield str(page), webpage + '/?page=' + str(page)


def sounds(html_content):
    webpage = 'https://www.myinstants.com'
    soup = BeautifulSoup(html_content, 'html.parser')
    titles = [title.getText()
              for title in soup.select('div[class="instant"] > a')]
    urls = [webpage + x.get('onclick').split("'")[1]
            for x in soup.select(
                'div[class="instant"] > div[class="small-button"]')]
    for url, title in zip(urls, titles):
        description = title
        yield url, title, description
