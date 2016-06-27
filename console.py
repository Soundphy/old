import os
import time
from importlib import import_module

from scraping.common import write_csv
from scraping.common import fill_index
from scraping.common import create_index
from scraping.common import download_html
from scraping.common import download_audio


SERVICES = {
    'soundfxcenter': [
        dict(name='starcraft',
             keywords='StarCraft, SC',
             url_path='/sound-effects/starcraft/'),
        dict(name='warcraft2',
             keywords='Warcraft 2, WC, Warcraft2',
             url_path='/sound-effects/warcraft-2/'),
        dict(name='terminator',
             keywords='Terminator',
             url_path='/sound-effects/terminator/'),
        dict(name='300',
             keywords='300',
             url_path='/sound-effects/300/'),
        dict(name='backtothefuture',
             keywords='Back to the Future',
             url_path='/sound-effects/back-to-the-future/'),
        dict(name='batman',
             keywords='Batman',
             url_path='/sound-effects/batman/'),
        dict(name='despicableme',
             keywords='Despicable Me',
             url_path='/sound-effects/despicable-me/'),
        dict(name='forrestgump',
             keywords='Forrest Gump',
             url_path='/sound-effects/forrest-gump/'),
        dict(name='harrypotter',
             keywords='Harry Potter',
             url_path='/sound-effects/harry-potter/'),
        dict(name='matrix',
             keywords='Matrix',
             url_path='/sound-effects/matrix/'),
        dict(name='starwars',
             keywords='Star Wars',
             url_path='/sound-effects/star-wars/'),
        dict(name='lotr',
             keywords='The Lord of the Rings, LotR',
             url_path='/sound-effects/the-lord-of-the-rings/'),
        dict(name='toystory',
             keywords='Toy Story',
             url_path='/sound-effects/toy-story/'),
        dict(name='walle',
             keywords='Wall-E, WallE',
             url_path='/sound-effects/wall-e/'),
        dict(name='supermario',
             keywords='Super Mario Bros',
             url_path='/sound-effects/super-mario-bros/'),
        dict(name='futurama',
             keywords='Futurama',
             url_path='/sound-effects/futurama/'),
        dict(name='simpsons',
             keywords='The Simpsons',
             url_path='/sound-effects/the-simpsons/'),
        dict(name='bigbang',
             keywords='The Big Bang Theory',
             url_path='/sound-effects/the-big-bang-theory/'),
        dict(name='southpark',
             keywords='South Park',
             url_path='/sound-effects/south-park/'),
        dict(name='tarzan',
             keywords='Tarzan',
             url_path='/sound-effects/tarzan/'),
        dict(name='startrek',
             keywords='Star Trek',
             url_path='/sound-effects/star-trek/'),
        dict(name='spongebob',
             keywords='Spongebob',
             url_path='/sound-effects/spongebob-squarepants/'),
        dict(name='flintstones',
             keywords='The Flintstones',
             url_path='/sound-effects/the-flintstones/'),
        dict(name='looneytunes',
             keywords='Looney Tunes',
             url_path='/sound-effects/looney-tunes/'),
        dict(name='familyguy',
             keywords='Family Guy',
             url_path='/sound-effects/family-guy/'),
        dict(name='disney',
             keywords='Disney',
             url_path='/sound-effects/disney/'),
    ],
    'dota2gamepedia': [
        dict(name='heroes',
             keywords='Dota 2, Dota2, Heroes',
             url_path='/Hero_Grid'),
    ],
    'springfieldfiles': [
        dict(name='sounds',
             keywords='The Simpsons',
             url_path='index.php?jump=sounds'),
    ],
    'instantsfun': [
        dict(name='sounds',
             keywords='',
             url_path='/'),
    ],
}


def process(service, section, html=False, csv=False, fill=False, audio=False):
    # Paths
    output_path = os.path.join('data', service+'_'+section['name'])
    html_dir = os.path.join(output_path, 'html')
    audio_dir = os.path.join(output_path, 'audio')
    csv_path = os.path.join(output_path, 'audio.csv')
    # Module import
    module = import_module('scraping.%s' % service)
    # Download
    if html:
        download_html(module.pages, section['url_path'], html_dir)
    if csv:
        write_csv(module.sounds, html_dir, csv_path, section['keywords'])
    if fill:
        fill_index('indexdir', csv_path)
    if audio:
        download_audio(csv_path, audio_dir)


if __name__ == '__main__':
    t0 = time.time()
    create_index('indexdir')
    for service, sections in SERVICES.items():
        for section in sections:
            process(service, section,
                    html=False, csv=False, fill=False, audio=False)
    t1 = time.time()
    print(t1 - t0)
