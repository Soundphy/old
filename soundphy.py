"""
Soundphy RESTful API.
"""
import inspect
import sqlite3
import traceback

from flask import Flask
from flask import abort
from flask import request
from flask import jsonify

from download import create_and_fill_database


DB_NAME = 'local.db'

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
    return jsonify(title='Soundphy RESTful API', versions=['v0'])


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
    db_connection = sqlite3.connect(DB_NAME)
    c = db_connection.cursor()
    db_query = 'SELECT url,description from test WHERE description IS ?'
    results = c.execute(db_query, (query,)).fetchall()
    results = [dict(url=x, description=y) for (x, y) in results]
    return jsonify(results=results)


@app.route('/v0/_download')
def _download():
    """
    Fill the database with new data.
    """
    try:
        create_and_fill_database(DB_NAME)
    except Exception:
        return jsonify(error=traceback.format_exc())
    return jsonify(finished='OK')


@app.route('/<path:path>', methods=['GET', 'POST'])
def _catch_all(path):
    abort(404, 'Requested API call does not exist')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, threaded=True, debug=True)
