#!/usr/bin/python3
"""
Auth module
"""
from db import DB
from sqlalchemy.exc import NoResultFound
import bcrypt


def _hash_password(password: str):
    """Hash password"""
    if password:
        salt = bcrypt.gensalt(10)
        return bcrypt.hashpw(password=password.encode('utf-8'), salt=salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize Auth
        """
        self._db = DB()

    def register_user(self, email: str, password: str):
        """Register a new user
        """
        try:
            old_user = self._db.find_user_by(email=email)
            if old_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            user = self._db.add_user(email, password=_hash_password(password))
            return user
