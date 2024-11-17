#!/usr/bin/env python3
"""Auth class for managing API Authentication"""
from typing import List, TypeVar
from flask import request
import re


class Auth:
    """Auth class fo authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """This function is used to require authentication"""
        if not (path and excluded_paths):
            return True

        if not path.endswith('/'):
            path = path + '/'

        for ep in excluded_paths:
            if '*' in ep:
                if path.startswith(ep.split('*')[0]):
                    return False

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request:
            if request.headers.get('Authorization', None):
                return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get current user"""
        return None
