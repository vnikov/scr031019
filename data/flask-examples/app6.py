from datetime import datetime
from uuid import uuid4

import flask
from flask import Flask, jsonify, request, abort


app = Flask(__name__)

state = {
    'posts': { }
#         uuid4().hex: {
#             'postedDate': datetime.utcnow(),
#             'authorName': 'rick',
#             'title': 'first!',
#             'body': 'First post!'
#         }
#     }
}

def url_for(*args, **kwargs):
    return flask.url_for(*args, _external=True, **kwargs)

@app.route('/')
def get_root():
    return jsonify(_links={'posts': url_for('get_posts')})

@app.route('/post')
def get_posts():
    post_links = [url_for('get_post', id=id) for id in state['posts']]
    return jsonify(
        _links={'self': url_for('get_posts')},
        data=[dict(_links=dict(self=link)) for link in post_links])

@app.route('/post', methods=['POST'])
def create_post():
    post_id = uuid4().hex
    post = {
        'postedDate': datetime.utcnow(),
        'authorName': request.authorization.username,
        **request.json
    }
    state['posts'][post_id] = post
    result = jsonify_post(post_id, post)
    result.headers['Location'] = url_for('get_post', id=post_id)
    return result, 201

@app.route('/post/<id>')
def get_post(id):
    post = state['posts'].get(id)
    if not post:
        abort(404)
    return jsonify_post(id, post)

@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    post = state['posts'].get(id)
    if not post:
        abort(404)
    post = {
        'postedDate': datetime.utcnow(),
        'authorName': request.authorization.username,
        **request.json
    }
    state['posts'][id] = post
    return jsonify_post(id, post)

@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    state['posts'].pop(id)
    return '', 204

def jsonify_post(id, post, **kwargs):
    return jsonify(
        _links={'self': url_for('get_post', id=id)},
        postedDate=post['postedDate'].isoformat(),
        authorName=post['authorName'],
        title=post['title'],
        body=post['body']
    )
    
