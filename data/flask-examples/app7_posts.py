from datetime import datetime
from uuid import uuid4

import flask
from flask import Blueprint, jsonify, request, abort

from .app7_util import state, url_for

mod = Blueprint('posts', __name__)

@mod.route('')
def get_root():
    post_links = [url_for('.get_post', id=id) for id in state['posts']]
    return jsonify(
        _links={
            'self': url_for('.get_root'),
            'home': url_for('get_root'),
        },
        data=[dict(_links=dict(self=link)) for link in post_links])

@mod.route('', methods=['POST'])
def create_post():
    post_id = uuid4().hex
    post = {
        'postedDate': datetime.utcnow(),
        'authorName': request.authorization.username,
        **request.json
    }
    state['posts'][post_id] = post
    result = jsonify_post(post_id, post)
    result.headers['Location'] = url_for('.get_post', id=post_id)
    return result

@mod.route('<id>')
def get_post(id):
    post = state['posts'].get(id)
    if not post:
        abort(404)
    return jsonify_posts(id, post)

@mod.route('<id>', methods=['PUT'])
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

@mod.route('<id>', methods=['DELETE'])
def delete_post(id):
    state['posts'].pop(id)
    return '', 204

def jsonify_post(id, post, **kwargs):
    return jsonify(
        _links={'self': url_for('.get_post', id=id)},
        postedDate=post['postedDate'].isoformat(),
        authorName=post['authorName'],
        title=post['title'],
        body=post['body']
    )
