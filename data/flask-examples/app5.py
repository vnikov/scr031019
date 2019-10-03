from datetime import datetime
from uuid import uuid4

import flask
from flask import Flask, jsonify, request, abort


app = Flask(__name__)

state = {
    'posts': {
        uuid4().hex: {
            'postedDate': datetime.utcnow(),
            'authorName': 'rick',
            'title': 'first!',
            'body': 'First post!'
        }
    }
}

def url_for(*args, **kwargs):
    return flask.url_for(*args, _external=True, **kwargs)

@app.route('/')
def get_root():
    return jsonify(_links={'posts': url_for('get_posts')})

@app.route('/post')
def get_posts():
    post_links = [
        url_for('get_post', id=id) 
        for id in state['posts']
    ]
    return jsonify(
        _links={'self': url_for('get_posts')},
        data=[
            dict(_links=dict(self=link)) 
            for link in post_links
        ]
    )

@app.route('/post/<id>')
def get_post(id):
    post = state['posts'].get(id)
    if not post:
        abort(404)
    return jsonify(
        _links={'self': url_for('get_post', id=id)},
        postedDate=post['postedDate'].isoformat(),
        authorName=post['authorName'],
        title=post['title'],
        body=post['body']
    )
