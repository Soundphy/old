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


@app.errorhandler(404)
def handle_400(error):
    return error_information(error)


@app.route('/')
def root():
    return jsonify(title='Soundphy RESTful API', versions=[0.1])


@app.route('/v0.1/reverse/<string:query>')
def reverse(query):
    return jsonify(reverse=query[::-1])


@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    abort(404, 'Requested API call does not exist')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
