import os
import re
import requests
from whoosh.fields import ID
from whoosh.fields import TEXT
from whoosh.fields import NGRAMWORDS
from whoosh.fields import Schema
from whoosh.index import create_in


def download_instantsfun_es():
    WEBPAGE = 'http://www.instantsfun.es'
    response = requests.get(WEBPAGE)
    response.raise_for_status()

    buttons = [x for x in response.text.split('\n') if 'type="audio' in x]
    descriptions = [re.findall('title="([^"]*)', x)[0] for x in buttons]
    urls = [WEBPAGE + re.findall('source src="([^"]*mp3)', x)[0]
            for x in buttons]

    return zip(urls, descriptions)


def create_schema(index_directory):
    schema = Schema(url=ID(stored=True),
                    title=TEXT(stored=True),
                    description=NGRAMWORDS(minsize=1))
    if not os.path.isdir(index_directory):
        os.makedirs(index_directory)
    ix = create_in(index_directory, schema)
    writer = ix.writer()
    for url, description in download_instantsfun_es():
        writer.add_document(url=url,
                            title=description,
                            description=description)
    writer.commit()


if __name__ == '__main__':
    PATH = 'indexdir'
    create_schema(PATH)
