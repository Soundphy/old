"""
Scraping module for instantsfun.
"""
import re

from bs4 import BeautifulSoup


def pages(route):
    webpage = 'http://www.instantsfun.es' + route
    name = 'all'
    yield name, webpage


def sounds(html_content):
    webpage = 'http://www.instantsfun.es'
    lines = html_content.split('\n')
    while len(lines):
        line = lines.pop()
        if 'class="description' not in line:
            continue
        description = BeautifulSoup(line, 'html.parser').text
        line = lines.pop()
        line = lines.pop()
        title = re.findall('title="([^"]*)', line)[0].strip()
        url = webpage + re.findall('source src="([^"]*mp3)', line)[0]
        yield dict(url=url, title=title, description=description)
