#!/usr/bin/env python3
"""
SessionAuth that inherits from Auth
"""
from uuid import uuid4

from requests import session
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None):
        """Creates a new authentication session"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = uuid4()
        __class__.user_id_by_session_id[session_id] = user_id

        return session_id
