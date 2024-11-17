#!/usr/bin/env python3
""" Module of session db auth """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import datetime


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class """
    def create_session(self, user_id=None):
        """ Create session """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        userSession = UserSession(user_id=user_id, session_id=session_id)
        userSession.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ User id for session id """
        if session_id is None or not isinstance(session_id, str):
            return None
        UserSession.load_from_file()
        userSession = UserSession.search({"session_id": session_id})
        if not userSession:
            return None
        created_at = userSession[0].created_at
        if created_at is None:
            return None
        now = datetime.datetime.now()
        duration = datetime.timedelta(seconds=self.session_duration)
        if now > created_at + duration:
            return None
        return userSession[0].user_id

    def destroy_session(self, request=None):
        """ Destroy session """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        userSession = UserSession.search({"session_id": session_id})
        if userSession:
            userSession[0].remove()
            return True
        return False
