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


@app.route('/profile', methods=['GET'], strict_slashes=False)
def get_profile():
    """Get current user's profile"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200

    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password():
    """Get user password resetting token
    """
    email = request.form.get('email')

    if email:
        try:
            token = AUTH.get_reset_password_token(email=email)
            if token:
                return jsonify({"email": email, "reset_token": token})
        except ValueError:
            pass

    abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_user_password():
    """Update a user's password through reset token
    """
    email = request.form.get('email')
    token = request.form.get('reset_token')
    new_pwd = request.form.get('new_password')

    if email and token:
        try:
            AUTH.update_password(reset_token=token,
                                 password=new_pwd)
            return jsonify({"email": email,
                            "message": "Password updated"}), 200

        except ValueError:
            abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
