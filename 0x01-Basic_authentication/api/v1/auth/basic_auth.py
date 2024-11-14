#!/usr/bin/env python3
"""BasicAuth that inherits from Auth"""

from base64 import b64decode
from typing import Tuple
from api.v1.auth.auth import Auth


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