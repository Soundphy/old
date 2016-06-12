import os
import soundphy


# TODO: database file is destroyed on deployment. Maybe it should be stored in
#       OPENSHIFT_DATA_DIR in the future (when the database is more stable)
soundphy.DB_NAME = os.path.join(os.path.dirname(__file__), 'local.db')
application = soundphy.app


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    HOST, PORT = 'localhost', 5000
    print('Serving at http://%s:%s' % (HOST, PORT))
    make_server(HOST, PORT, application).serve_forever()
