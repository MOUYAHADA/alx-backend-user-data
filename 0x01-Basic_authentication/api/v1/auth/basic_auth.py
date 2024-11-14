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

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on
        his email and password."""
        if user_email and user_email and\
                type(user_email) is str and type(user_pwd) is str:

            if User.count():
                result = User.search({'email': user_email})

                if len(result):
                    user = result[0]
                    if User.is_valid_password(user, user_pwd):
                        return user

        return None
