"""
Soundphy RESTful API.
"""
import random
import inspect
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.sorting import FieldFacet

from flask import Flask
from flask import abort
from flask import request
from flask import jsonify


INDEXDIR = 'indexdir'

app = Flask('Soundphy')


def list_routes(app, starting=''):
    output = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith('_'):
            continue
        if not str(rule).startswith(starting):
            continue
        output.append(dict(
            name=rule.endpoint,
            rule=rule.rule,
            methods=','.join(rule.methods),
            doc=inspect.getdoc(app.view_functions[rule.endpoint])
        ))
    return output


def error_information(error):
    info = {}
    info['code'] = error.code
    info['name'] = error.name
    if error.response:
        info['response'] = error.response
    if error.description:
        info['description'] = error.description
    return jsonify(error=info), error.code


@app.errorhandler(400)
def handle_400(error):
    return error_information(error)


@app.errorhandler(404)
def handle_400(error):
    return error_information(error)


@app.route('/')
def root():
    versions = dict(v0=request.url+'v0')
    return jsonify(title='Soundphy RESTful API', versions=versions)


@app.route('/v0')
def routes():
    return jsonify(routes=list_routes(app, '/v0'))


@app.route('/v0/reverse/<string:query>')
def reverse(query):
    """
    Return the reversed query string provided (for testing purposes).
    """
    return jsonify(reverse=query[::-1])


@app.route('/v0/search/<string:query>')
def search(query):
    """
    Search for a sound file in the Soundphy service.
    """
    ix = open_dir(INDEXDIR)
    with ix.searcher() as searcher:
        section_facet = FieldFacet('section')
        s = searcher.search(
            QueryParser('query', ix.schema).parse(query),
            collapse=section_facet)
        results = [dict(x) for x in s]
    return jsonify(results=results)


@app.route('/v0/popular')
def popular():
    """
    Return the most popular sounds.
    """
    popular = [
        'eec6e23d7367029c438c633cdab59ea81a17a903',
        'f3a1589b686014a6edf79626c8ce3ecc36d70caf',
        '8ac748e7a6f92c197e5c1663fc0efa8dceb09f7a',
        '2d0dd9f34f0201ebeb9426cf32f768cfa20e4c99',
        '2db977651d33cab5b7696101273f0799bb30a7fa',
        'eadb1b7155669cee75207fc5065ab4a4389ef3d4',
        'aed7186c425e07c943136f54e8b2455c922c7aa5',
        '071da343b02eef4ecbb9fdd7f3b6995f3775a019',
        '2f11958a33d410463b98b2aeda175296e2b441a6',
        'e30a33e0afc550f41c2e65a47fefc0876496791e',
        'dfe4714f47e43f8cb97a257bfc74268cd973f68c',
        '3a8cf482014b036241c243c61906bbb433921ffc',
        '3cd07bf67b782609f7a959b13036d90dbf01c320',
        '5784880dd20bb4c23b15daf013c2f9f6f73f1344',
        'b42a7899b5604ec33a8976aafa9ecb7d27e6b2cf',
        'd548c1e8c742af833663dfb11e4d1cb5cfda6f2d',
        'c4c2e62f06880ed1b71d98e04ace2cde874ba3bc',
        '284e4810deaf930f3418bcbdb95d4520b07ebf26',
        'fbb08fd5885b5f496a886bd0ed1b75eaf8ff7d27',
        '399868f0f88de4dd1881560524c3bf9e940437ae',
        '4ab991a2fc9d574cba0496d876f6c94b31cafe2a',
        '27a4d8aeb117450545dfd5d2bf124f1b82e814e6',
        'e0b843193d1c1c4134109586203315080cf864f2',
        '86518c30ddf15ff7c6b4539fd8af626facfc65bc',
        '2f3e2776c01ff20ec22b88e26a8dc54ed92c53b7',
        '325230dba6c8946aeebd2365e8e4b501d65d51be',
    ]
    random.shuffle(popular)
    ix = open_dir(INDEXDIR)
    with ix.searcher() as searcher:
        results = [searcher.document(identifier=x) for x in popular]
    return jsonify(results=results)


@app.route('/<path:path>', methods=['GET', 'POST'])
def _catch_all(path):
    abort(404, 'Requested API call does not exist')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, threaded=True, debug=True)
