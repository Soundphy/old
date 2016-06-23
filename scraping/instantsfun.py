"""
Scraping module for instantsfun.
"""
import os
import re
import csv
from hashlib import sha1

import requests
from bs4 import BeautifulSoup


def urls(route):
    webpage = 'http://www.instantsfun.es' + route
    name = 'all'
    yield name, webpage


def parse_html(html_directory, csv_path, keywords):
    webpage = 'http://www.instantsfun.es'
    with open(csv_path, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(['identifier', 'url', 'title', 'description'])
        kwlist = [x.strip() for x in keywords.split(',')]
        for fname in os.listdir(html_directory):
            with open(os.path.join(html_directory, fname)) as fin:
                text = fin.read()
            lines = text.split('\n')
            while len(lines):
                line = lines.pop()
                if not 'class="description' in line:
                    continue
                description = BeautifulSoup(line, 'html.parser').text
                line = lines.pop()
                line = lines.pop()
                title = re.findall('title="([^"]*)', line)[0].strip()
                url = webpage + re.findall('source src="([^"]*mp3)', line)[0]
                identifier = sha1(url.encode('ascii')).hexdigest()
                full_title = title + ' ' + description
                writer.writerow([identifier, url, full_title, full_title])
