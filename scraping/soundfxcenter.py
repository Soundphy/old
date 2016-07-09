"""
Scraping module for soundfxcenter.
"""
import re

import requests
from bs4 import BeautifulSoup


def pages(route):
    webpage = 'http://soundfxcenter.com' + route
    response = requests.get(webpage + '0')
    response.raise_for_status()
    try:
        last = int(re.findall('\/([0-9]*)">>>', response.text)[-1])
    except IndexError:
        last = 0
    for i in range(0, last + 10, 10):
        yield str(i), webpage + str(i)


def sounds(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for audio in soup.find_all('audio'):
        url = audio.attrs['src']
        title = audio.find_previous('table').find('strong').text
        if title.lower().endswith(' sound effect'):
            title = title[:-len(' sound effect')]
        yield dict(url=url, title=title)
