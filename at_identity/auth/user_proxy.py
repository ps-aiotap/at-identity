"""
Proxy user object that doesn't require database storage
"""

class ATIdentityUser:
    """Virtual user object backed by AT Identity service"""
    
    def __init__(self, user_data):
        self.id = user_data['id']
        self.username = user_data['username']
        self.email = user_data['email']
        self.first_name = user_data.get('first_name', '')
        self.last_name = user_data.get('last_name', '')
        self.is_active = user_data.get('is_active', True)
        self.is_authenticated = True
        self.is_anonymous = False
        self._permissions = set(user_data.get('permissions', []))
    
    def has_perm(self, permission):
        return permission in self._permissions
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def __str__(self):
        return self.username