#!/usr/bin/env python3
"""BasicAuth that inherits from Auth"""

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
