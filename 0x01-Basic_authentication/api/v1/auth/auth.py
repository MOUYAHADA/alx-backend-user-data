#!/usr/bin/env python3
"""Auth class for managing API Authentication"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Auth class fo authentication"""

    def require_auth(self, path: str, exclude_paths: List[str]) -> bool:
        """This function is used to require authentication"""
        return False

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get current user"""
        return None
