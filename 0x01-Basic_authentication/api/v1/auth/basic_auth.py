#!/usr/bin/env python3
""" Baic Authentication Module """
from api.v1.auth.auth import Auth
from models.user import User
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
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """ Extract user credentials (Email and Password)
        """
        if not decoded_base64_authorization_header:
            return (None, None)
        elif type(decoded_base64_authorization_header) != str:
            return (None, None)
        elif ":" not in decoded_base64_authorization_header:
            return (None, None)
        else:
            user_list = decoded_base64_authorization_header.split(":")
            return (user_list[0], user_list[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """ Retrieve User object from credentials
        """
        if not user_email or type(user_email) != str:
            return None
        elif not user_pwd or type(user_pwd) != str:
            return None
        user = User.search({"email": user_email})
        if not user:
            return None
        if user.is_valid_password(user_pwd):
            return user
        return None
