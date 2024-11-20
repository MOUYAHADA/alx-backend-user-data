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

    def create_session(self, email: str) -> str:
        """Finds the user corresponding to the email, generate a new UUID
        and store it in the database as the user’s session_id"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Takes a single session_id string argument
        Returns:
            User: the corresponding User or None"""
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None

    def destroy_session(self, user_id: int) -> None:
        """Updates the corresponding user’s session ID to None"""
        if type(user_id) is int:
            try:
                self._db.update_user(user_id=user_id, session_id=None)
            except ValueError:
                pass

    def get_reset_password_token(self, email: str) -> str:
        """Get a token for resetting user password
        Returns:
            str: reset token"""
        if email:
            try:
                user = self._db.find_user_by(email=email)
                token = _generate_uuid()
                self._db.update_user(user.id, reset_token=token)
                return token
            except NoResultFound:
                raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update a user's password using a token"""
        if reset_token and password:
            try:
                user = self._db.find_user_by(reset_token=reset_token)
                self._db.update_user(user_id=user.id,
                                     hashed_password=_hash_password(password),
                                     reset_token=None)
            except NoResultFound:
                raise ValueError
