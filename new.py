from importlib import import_module

from scraping.common import *


SERVICES = {
    'soundfxcenter': [
        dict(name='starcraft',
             keywords='StarCraft, SC',
             route='/sound-effects/starcraft/'),
        dict(name='warcraft2',
             keywords='Warcraft 2, WC, Warcraft2',
             route='/sound-effects/warcraft-2/'),
        dict(name='terminator',
             keywords='Terminator',
             route='/sound-effects/terminator/'),
        dict(name='300',
             keywords='300',
             route='/sound-effects/300/'),
        dict(name='backtothefuture',
             keywords='Back to the Future',
             route='/sound-effects/back-to-the-future/'),
        dict(name='batman',
             keywords='Batman',
             route='/sound-effects/batman/'),
        dict(name='despicableme',
             keywords='Despicable Me',
             route='/sound-effects/despicable-me/'),
        dict(name='forrestgump',
             keywords='Forrest Gump',
             route='/sound-effects/forrest-gump/'),
        dict(name='harrypotter',
             keywords='Harry Potter',
             route='/sound-effects/harry-potter/'),
        dict(name='matrix',
             keywords='Matrix',
             route='/sound-effects/matrix/'),
        dict(name='starwars',
             keywords='Star Wars',
             route='/sound-effects/star-wars/'),
        dict(name='lotr',
             keywords='The Lord of the Rings, LotR',
             route='/sound-effects/the-lord-of-the-rings/'),
        dict(name='toystory',
             keywords='Toy Story',
             route='/sound-effects/toy-story/'),
        dict(name='walle',
             keywords='Wall-E, WallE',
             route='/sound-effects/wall-e/'),
        dict(name='supermario',
             keywords='Super Mario Bros',
             route='/sound-effects/super-mario-bros/'),
        dict(name='futurama',
             keywords='Futurama',
             route='/sound-effects/futurama/'),
        dict(name='simpsons',
             keywords='The Sympsons',
             route='/sound-effects/the-simpsons/'),
        dict(name='bigbang',
             keywords='The Big Bang Theory',
             route='/sound-effects/the-big-bang-theory/'),
        dict(name='southpark',
             keywords='South Park',
             route='/sound-effects/south-park/'),
        dict(name='tarzan',
             keywords='Tarzan',
             route='/sound-effects/tarzan/'),
        dict(name='startrek',
             keywords='Star Trek',
             route='/sound-effects/star-trek/'),
        dict(name='spongebob',
             keywords='Spongebob',
             route='/sound-effects/spongebob-squarepants/'),
        dict(name='flintstones',
             keywords='The Flintstones',
             route='/sound-effects/the-flintstones/'),
        dict(name='looneytunes',
             keywords='Looney Tunes',
             route='/sound-effects/looney-tunes/'),
        dict(name='familyguy',
             keywords='Family Guy',
             route='/sound-effects/family-guy/'),
        dict(name='disney',
             keywords='Disney',
             route='/sound-effects/disney/'),
    ],
    'dota2gamepedia': [
        dict(name='heroes',
             keywords='Dota 2, Dota2, Heroes',
             route='/Hero_Grid'),
    ]
}


if __name__ == '__main__':
#    create_index('indexdir')
    for service, sections in SERVICES.items():
        for section in sections:
            # Paths
            output_path = os.path.join('data', service+'_'+section['name'])
            html_dir = os.path.join(output_path, 'html')
            audio_dir = os.path.join(output_path, 'audio')
            csv_path = os.path.join(output_path, 'audio.csv')
            # Module import
            module = import_module('scraping.%s' % service)
            # Download
#            module.download_html(section['route'], html_dir)
#            module.parse_html(html_dir, csv_path, section['keywords'])
            fill_index('indexdir', csv_path)
#            download_audio(csv_path, audio_dir)
