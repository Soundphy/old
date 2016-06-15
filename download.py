import os
import re
import requests
from bs4 import BeautifulSoup
from whoosh.fields import ID
from whoosh.fields import TEXT
from whoosh.fields import NGRAMWORDS
from whoosh.fields import Schema
from whoosh.index import create_in
from whoosh.writing import BufferedWriter


def download_instantsfun_es():
    WEBPAGE = 'http://www.instantsfun.es'
    response = requests.get(WEBPAGE)
    response.raise_for_status()

    buttons = [x for x in response.text.split('\n') if 'type="audio' in x]
    descriptions = [re.findall('title="([^"]*)', x)[0] for x in buttons]
    urls = [WEBPAGE + re.findall('source src="([^"]*mp3)', x)[0]
            for x in buttons]

    return zip(urls, descriptions)


def download_dota2_gamepedia_com():
    WEBPAGE = 'http://dota2.gamepedia.com'

    # Heroes
    response = requests.get(WEBPAGE + '/Hero_Grid')
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    heroes = soup.find_all('div', attrs={'style': 'position: relative;'})

    for hero in heroes:
        page = hero.find('a').attrs['href']
        name = hero.find('a').attrs['title']
        face = hero.find('img').attrs['src']
        response = requests.get(WEBPAGE + page + '/Responses')
        try:
            response.raise_for_status()
        except Exception:
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', attrs={'title': 'Play'})
        sounds = [link.attrs['href'] for link in links]
        descriptions = [link.parent.text.strip(' Play ') for link in links]
        yield (name, face, zip(sounds, descriptions))


def create_schema(index_directory):
    schema = Schema(url=ID(stored=True),
                    title=TEXT(stored=True),
                    description=NGRAMWORDS(minsize=1))
    if not os.path.isdir(index_directory):
        os.makedirs(index_directory)
    ix = create_in(index_directory, schema)
    writer = BufferedWriter(ix, period=30, limit=50)
    for url, description in download_instantsfun_es():
        writer.add_document(url=url,
                            title=description,
                            description=description)
    for name, face, responses in download_dota2_gamepedia_com():
        for sound, description in responses:
            writer.add_document(url=sound,
                                title='Dota2 %s '%name+description,
                                description='Dota2 %s '%name+description)


if __name__ == '__main__':
    PATH = 'indexdir'
    create_schema(PATH)
