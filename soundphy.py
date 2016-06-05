from flask import Flask


app = Flask('Soundphy')


@app.route('/')
def root():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
