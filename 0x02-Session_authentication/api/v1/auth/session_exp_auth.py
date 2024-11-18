#!/usr/bin/env python3
"""Module for SessionExpAuth class"""
import datetime
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class:
    for managing session expiration date"""

    def __init__(self) -> None:
        """Initialize super class"""
        super().__init__()
        session_duration = os.getenv('SESSION_DURATION')
        self.session_duration = int(session_duration)\
            if session_duration else 0

    def create_session(self, user_id: str = None):
        """Creates a new session for user"""
        session_id = super().create_session(user_id)
        if session_id:
            session_dict = {"user_id": user_id,
                            "created_at": datetime.datetime.now()}
            __class__.user_id_by_session_id[session_id] = session_dict
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns User Id if session is not expired"""
        if session_id:
            session = __class__.user_id_by_session_id.get(session_id, None)
            if session:
                if self.session_duration <= 0:
                    return session.get('user_id')
                created_at = session.get('created_at', None)

                if created_at:
                    exp_date = created_at + datetime.timedelta(
                        seconds=self.session_duration)

                    if exp_date > datetime.datetime.now():
                        return session.get('user_id')
