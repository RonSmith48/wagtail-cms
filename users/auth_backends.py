import requests
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from users.models import RemoteUser

class RemoteAuthBackend(BaseBackend):
    """
    Authenticate against the external auth server.
    """

    def authenticate(self, request, username=None, password=None):
        # POST to your auth-server’s login endpoint:
        try:
            print(f"Authenticating user {username} with password {password}")
            url = settings.AUTH_SERVER_URL.rstrip('/') + '/users/login/'
            resp = requests.post(
                url,
                json={'email': username, 'password': password},
                timeout=5
            )
        except requests.RequestException:
            return None
        
        data = resp.json()
        print('Response from auth server:', data)
        if resp.status_code == 200:
            token = data.get('tokens', {}).get('access') 
            profile = data.get('user')
            print('profile', profile)

            user, created = RemoteUser.objects.get_or_create(
                id=profile['id'],
                defaults = {
                    'first_name': profile['first_name'],
                    'last_name': profile['last_name'],
                    'initials': profile['initials'],
                    'email': profile['email'],
                    'is_staff': profile['is_staff'],
                    'is_active': profile['is_active'],
                    'is_superuser': profile['is_superuser'],
                    'start_date': profile['start_date'],
                    'role': profile['role'],
                    'permissions': profile['permissions'],
                    'avatar': profile['avatar'],
                }
            )
            return user

        return None

    def get_user(self, user_id):
        try:
            return RemoteUser.objects.get(id=user_id)
        except RemoteUser.DoesNotExist:
            return None
