#!/usr/bin/env python3
""" Baic Authentication Module """
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ Class definition of BasicAuth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """ Extract authorization header
        """
        if not authorization_header:
            return None
        elif type(authorization_header) != str:
            return None
        elif not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """ Check if header is valid
        """
        if not base64_authorization_header:
            return None
        elif not isinstance(base64_authorization_header, str):
            return None

        try:
            # Convert string to bytes and decode Base64.
            # Can only use base64 to decode uft-8 encoded str.
            base64_bytes = base64_authorization_header.encode('utf-8')
            message_bytes = base64.b64decode(base64_bytes)

            return message_bytes.decode('utf-8')
        except Exception as e:
            print(str(e))
            return None
