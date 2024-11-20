#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Home page"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """End-point to register a user"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Creates a new session for user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:

        if AUTH.valid_login(email, password):

            session_id = AUTH.create_session(email)
            res = jsonify({"email": email, "message": "logged in"})
            res.set_cookie('session_id', session_id)

            return res

    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Find the user with the requested session ID. If the user exists
    destroy the session and redirect the user to GET /"""
    session_id = request.cookies.get('session_id')
    if session_id:
        try:
            user = AUTH.get_user_from_session_id(session_id)
            AUTH.destroy_session(user.id)
            return redirect('/')
        except ValueError:
            pass

    abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
