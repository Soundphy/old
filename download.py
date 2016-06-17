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


def download_springfieldfiles_com():
    WEBPAGE = 'http://www.springfieldfiles.com/'
    response = requests.get(WEBPAGE + 'index.php?jump=sounds')
    response.raise_for_status()

    for line in response.text.split('\n'):
        aux = re.findall('<td width=..%.*<font size=3>([^<]*)<.*', line)
        if not aux:
            aux = re.findall('<td width=20%>([^<]*)</td>', line)
        if aux:
            name = aux[0]
            continue
        aux = re.findall('<td width=..%><a href="([^"]*)"', line)
        if not aux:
            continue
        url = aux[0]
        response = requests.get(WEBPAGE + url)
        try:
            response.raise_for_status()
        except Exception:
            continue
        sounds = []
        descriptions = []
        lines = response.text.split('\n')[::-1]
        while len(lines):
            line = lines.pop()
            sound = re.findall('href="(sounds[^"]*.mp3)">.*', line)
            if not sound:
                continue
            line = lines.pop()
            description = BeautifulSoup(line, 'html.parser').text
            if not description:
                continue
            sounds.append(WEBPAGE + sound[0])
            descriptions.append(description.strip('"'))
        yield (name, zip(sounds, descriptions))


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
    writer = BufferedWriter(ix, period=30, limit=1000)
    for url, description in download_instantsfun_es():
        writer.add_document(url=url,
                            title=description,
                            description=description)
    for name, sounds in download_springfieldfiles_com():
        for url, description in sounds:
            writer.add_document(url=url,
                                title='Simpsons %s '%name+description,
                                description='Simpsons %s '%name+description)
    for name, face, responses in download_dota2_gamepedia_com():
        for sound, description in responses:
            writer.add_document(url=sound,
                                title='Dota2 %s '%name+description,
                                description='Dota2 %s '%name+description)


if __name__ == '__main__':
    PATH = 'indexdir'
    create_schema(PATH)
