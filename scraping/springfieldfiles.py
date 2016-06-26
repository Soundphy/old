"""
Scraping module for springfieldfiles.
"""
import re

import requests
from bs4 import BeautifulSoup


def pages(route):
    webpage = 'http://www.springfieldfiles.com/'
    response = requests.get(webpage + route)
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
        fname = name + '_' + url.split('sounds/')[-1]
        yield fname, webpage + url


def sounds(html_content):
    webpage = 'http://www.springfieldfiles.com/'
    lines = html_content.split('\n')[::-1]
    while len(lines):
        line = lines.pop()
        sound = re.findall('href="(sounds[^"]*.mp3)">.*', line)
        if not sound:
            continue
        line = lines.pop()
        title = BeautifulSoup(line, 'html.parser').text
        if not title:
            continue
        url = webpage + sound[0]
        title = title.strip('"')
        description = title
        yield url, title, description
