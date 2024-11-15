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
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            user = User.search({'email': user_email})
            if user is None or len(user) == 0:
                return None
            user = user[0]
            if user.is_valid_password(user_pwd):
                return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user """
        auth = self.authorization_header(request)
        base64_auth = self.extract_base64_authorization_header(auth)
        decoded_base64_auth = self.decode_base64_authorization_header(
            base64_auth)
        user_email, user_pwd = self.extract_user_credentials(
            decoded_base64_auth)
        return self.user_object_from_credentials(user_email, user_pwd)
