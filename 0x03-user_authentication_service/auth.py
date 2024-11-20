#!/usr/bin/env python3
"""
Auth module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from db import DB
from user import User
import bcrypt
import uuid


def _hash_password(password: str) -> str:
    """Takes in password string argument
    Returns bytes(salted_hashed)
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize Auth
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user
        Takes mandatory string (email, password) arguments
        Returns a User object
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            user = self._db.add_user(
                email=email,
                hashed_password=_hash_password(password))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check a login and if it's valid return True"""
        if email and password:
            try:
                user = self._db.find_user_by(email=email)
                return bcrypt.checkpw(password.encode('utf-8'),
                                      user.hashed_password)
            except NoResultFound:
                return False
        return False
