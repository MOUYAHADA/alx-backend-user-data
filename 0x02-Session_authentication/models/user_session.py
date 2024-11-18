#!/usr/bin/env python3
"""Module for the UserSession model"""
from models.base import Base


class UserSession(Base):
    """User Session to be stored in database"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize class with base properties"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
