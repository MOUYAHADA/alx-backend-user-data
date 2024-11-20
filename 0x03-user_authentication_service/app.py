#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify, request
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
