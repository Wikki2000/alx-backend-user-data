#!/usr/bin/env python3
""" Authentication Module """
from typing import TypeVar, List


class Auth:
    """ Auth class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check path that require auth """
        return False

    def authorization_header(self, request=None) -> str:
        """ Check authorization header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Check current user """
        return None
