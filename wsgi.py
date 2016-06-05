from soundphy import app as application


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    HOST, PORT = 'localhost', 5000
    print('Serving at http://%s:%s' % (HOST, PORT))
    make_server(HOST, PORT, application).serve_forever()
