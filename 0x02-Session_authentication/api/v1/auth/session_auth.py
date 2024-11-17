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
        session_id = str(uuid4())
        __class__.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None or type(session_id) is not str:
            return None
        return __class__.user_id_by_session_id.get(session_id, None)
