#!/usr/bin/env python3
"""BasicAuth that inherits from Auth"""

from base64 import b64decode
import email
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract authorization header"""

        if (authorization_header is None) \
                or (type(authorization_header) is not str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.replace('Basic ', '').strip()

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """returns the decoded value of a Base64
        string base64_authorization_header"""
        if (base64_authorization_header is None)\
                or (type(base64_authorization_header) is not str):
            return None

        try:
            header = b64decode(base64_authorization_header.encode('utf-8'))
        except Exception:
            return None

        return header.decode('utf-8')

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """returns the user email and password
        from the Base64 decoded value."""

        d = decoded_base64_authorization_header

        if (d is None) or (type(d) is not str) or (':' not in d):
            return None, None

        email, password = d.split(":")
        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on
        his email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves
        the User instance for a request_
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        user = self.user_object_from_credentials(
                            email, password)
                        if user is not None:
                            return user

        return
