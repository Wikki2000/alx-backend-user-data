#!/usr/bin/env python3
"""Authentication Module
"""
import bcrypt
from db import DB
from sqlalchemy.exc import NoResultFound
from user import User
from uuid import uuid4


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user in database,
        If user exists already raise ValueError
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash_pwd = _hash_password(password)
            user = self._db.add_user(email=email, hashed_password=hash_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user credentials
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), user.hashed_password)


def _hash_password(password: str) -> bytes:
    """Hash user password for security purposes.

    :password - The password to be hash.
    :rtype - The hash password in bytes
    """
    if password and isinstance(password, str):
        # Can only hash encoded string using bcrypt
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return None


def _generate_uuid() -> str:
    """Generate a new UUID
    """
    return str(uuid4())
