"""
Soundphy RESTful API.
"""
import inspect
import traceback
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

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
        results = [dict(x) for x in searcher.search(
            QueryParser('query', ix.schema).parse(query)
        )]
    return jsonify(results=results)


@app.route('/<path:path>', methods=['GET', 'POST'])
def _catch_all(path):
    abort(404, 'Requested API call does not exist')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, threaded=True, debug=True)
