from flask import Flask
from flask import Response


# this is the flask app that will be run on wsgi
# as with pyramid, u don't need to touch the server, it'll adapt

flask_app = Flask('flaskapp')


@flask_app.route('/hello')
def order():
    return Response('I asking for 5FQ from Flask!\n', mimetype='text/plain')


# The app is a new wsgi app, from the flask lib
app = flask_app.wsgi_app
