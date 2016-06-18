"""
Common scraping classes and functions.
"""
import os
from csv import DictReader

import requests
from whoosh.fields import TEXT
from whoosh.fields import STORED
from whoosh.fields import NGRAMWORDS
from whoosh.fields import Schema
from whoosh.index import open_dir
from whoosh.index import create_in


def download_file(url, output_path):
    response = requests.get(url, stream=True)
    with open(output_path, 'wb') as fout:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                fout.write(chunk)


def create_index(index_directory):
    schema = Schema(identifier=STORED,
                    url=STORED,
                    title=STORED,
                    description=NGRAMWORDS(minsize=2))
    os.makedirs(index_directory, exist_ok=True)
    create_in(index_directory, schema)


def download_audio(csv_path, output_directory):
    os.makedirs(output_directory, exist_ok=True)
    finput = DictReader(open(csv_path))
    for row in finput:
        output_path = os.path.join(output_directory, row['identifier'])
        if os.path.isfile(output_path):
            continue
        print(output_path)
        download_file(row['url'], output_path)


def fill_index(index_directory, csv_path):
    index = open_dir(index_directory)
    writer = index.writer()
    finput = DictReader(open(csv_path))
    for row in finput:
        writer.update_document(identifier=row['identifier'],
                               url=row['url'],
                               title=row['title'],
                               description=row['description'])
    writer.commit()
