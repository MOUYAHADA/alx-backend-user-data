#!/usr/bin/env python3
"""Module for user authentication using session
IDs stored in cookies."""
import os
from flask.json import jsonify
from api.v1.auth.session_auth import SessionAuth
from api.v1.views import app_views
from flask import request

from models.user import User


@app_views.post('/auth_session/login', strict_slashes=False)
def login():
    """Login function that authenticates a user and creates a session.

    This function retrieves the user's email and password from the request,
    validates them, and if successful, creates a session ID stored in a cookie.

    Returns:
        Response: A JSON response containing user information or an error message.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})

    if not len(users):
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    user = user.to_json(True)
    session = SessionAuth().create_session(user.get('id'))

    res = jsonify(user)
    session_name = os.getenv('SESSION_NAME')
    res.set_cookie(session_name, session)

    return res
