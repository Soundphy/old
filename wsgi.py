"""
Web Server Gateway Interface.
"""
import os
import soundphy


DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', os.path.dirname(__file__))
soundphy.INDEXDIR = os.path.join(DATA_DIR, soundphy.INDEXDIR)
application = soundphy.app


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    HOST, PORT = 'localhost', 5000
    print('Serving at http://%s:%s' % (HOST, PORT))
    make_server(HOST, PORT, application).serve_forever()
