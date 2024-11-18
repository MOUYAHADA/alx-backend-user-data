#!/usr/bin/env python3
"""Module for the SesssionDBAuth class"""


from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Authenticate users from sessions stored in the DB"""

    def create_session(self, user_id: str = None):
        """
        Creates a new authentication session
        Returns:
            str: session id
        """
        if user_id:
            session_id = super().create_session(user_id)
            session = UserSession(user_id=user_id, session_id=session_id)
            session.save()
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Get user id for session id
        Returns:
            str: user id
        """
        if session_id is not None and type(session_id) is str:
            try:
                sessions = UserSession.search({"session_id": session_id})

                if len(sessions):
                    [session] = sessions

                    if self.session_duration <= 0:
                        return session.user_id

                    exp_date = session.created_at + \
                        timedelta(seconds=self.session_duration)

                    if exp_date > datetime.utcnow():
                        return session.user_id
                    else:
                        from flask import request
                        self.destroy_session(request)
            except Exception:
                return None

    def destroy_session(self, request=None):
        """Destroy a session and delete it from DB
        Returns:
            str: Session ID"""
        if request:
            session_id = self.session_cookie(request)

            if session_id is not None:
                session = UserSession.get(session_id)
                if session:
                    session.remove()
                super().destroy_session(request)
                return session_id
