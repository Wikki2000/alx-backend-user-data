#!/usr/bin/env python3
""" Authentication Module """
from typing import TypeVar, List
from flask import request


class Auth:
    """ Auth class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check path that require auth """
        if not path or not excluded_paths:
            return True

        if path in excluded_paths or path + "/" in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """ Check authorization header """
        if not request:
            return None

        # Return value of headers if found, else None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ Check current user """
        return None
