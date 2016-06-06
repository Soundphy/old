"""
Soundphy RESTful API.
"""
from flask import Flask
from flask import abort
from flask import request
from flask import jsonify


app = Flask('Soundphy')


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


@app.route('/')
def root():
    return 'Hello World!'


@app.route('/v0.1/reverse')
def reverse():
    query = request.args.get('query')
    if query is None:
        abort(400, 'Missing required parameter `query`')
    return jsonify(reverse=query[::-1])


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
