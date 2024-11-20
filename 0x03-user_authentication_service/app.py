#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Home page"""
    return jsonify({"message": "Bienvenue"})
