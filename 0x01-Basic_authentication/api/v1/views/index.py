#!/usr/bin/env python3
""" Module of Index views
"""
from operator import truediv
from flask import jsonify, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/users', strict_slashes=False)
def users() -> str:
    """ GET /api/v1/users
    Return:
      - the number of users
    """
    users_list = []
    users = User.all()
    for user in users:
        user_dict = user.to_json(True)
        del user_dict['_password']
        users_list.append(user_dict)

    return jsonify(users_list)


@app_views.route('/unauthorized', strict_slashes=False)
def unauthorized() -> str:
    """ GET /api/v1/unauthorized
    Return:
      401 error: Unauthorized
    """
    abort(401)


@app_views.route('/forbidden', strict_slashes=False)
def forbidden() -> str:
    """ GET /api/v1/forbidden
    Return:
      401 error: Forbidden
    """
    abort(403)
