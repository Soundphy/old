"""
Soundphy RESTful API.
"""
from flask import Flask
from flask import abort
from flask import request
from flask import jsonify


app = Flask('Soundphy')


@app.errorhandler(400)
def handle_400(e):
    return jsonify(error=str(e)), 400


@app.route('/')
def root():
    return 'Hello World!'


@app.route('/api/v0.1/reverse')
def reverse():
    query = request.args.get('query')
    if query is None:
        abort(400)
    return jsonify(reverse=query[::-1])


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
