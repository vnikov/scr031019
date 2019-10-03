import flask

app = flask.Flask(__name__)

@app.route('/')
def get_root():
    return flask.jsonify(hello='world')

@app.route('/<name>')
def get_name(name):
    return flask.jsonify(hello=name)
