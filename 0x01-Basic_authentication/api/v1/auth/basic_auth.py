#!/usr/bin/env python3
""" Baic Authentication Module """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Class definition of BasicAuth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Extract authorization header
        """
        if not authorization_header:
            return None
        elif type(authorization_header) != str:
            return None
        elif not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]
