#!/usr/bin/python3
"""
Auth module
"""
import bcrypt


def _hash_password(password: str):
    """Hash password"""
    if password:
        salt = bcrypt.gensalt(10)
        return bcrypt.hashpw(password=password.encode('utf-8'), salt=salt)
