"""
Custom session backend for userless authentication
"""
from django.contrib.sessions.backends.base import SessionBase
import json

class ATIdentitySessionStore(SessionBase):
    """Session store that handles AT Identity user data"""
    
    def load(self):
        try:
            session_data = self._get_session_from_db()
            return self.decode(session_data)
        except:
            self._session_key = None
            return {}
    
    def exists(self, session_key):
        return bool(session_key and self._get_session_from_db())
    
    def create(self):
        while True:
            self._session_key = self._get_new_session_key()
            try:
                self.save(must_create=True)
            except:
                continue
            self.modified = True
            return
    
    def save(self, must_create=False):
        """Save session data"""
        # Store in cache/database as needed
        pass
    
    def delete(self, session_key=None):
        """Delete session"""
        pass
    
    def _get_session_from_db(self):
        """Get session data from storage"""
        return None