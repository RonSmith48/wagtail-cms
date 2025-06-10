
import requests
import sys
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from users.models import RemoteUser

# How often you consider a local copy “stale” (you can ignore TTL if you only
# want to fetch-once). For now, set it very long (e.g. 1 day):
USER_CACHE_TTL = timedelta(days=1)


def fetch_user_from_auth_server(user_id, token):
    """
    Call GET <AUTH_SERVER_URL>/users/user/<user_id>/,
    return the JSON dict, or None on failure.
    """
    url = f"{settings.AUTH_SERVER_URL.rstrip('/')}/users/user/{user_id}/"
    # Ensure token is a str, not bytes:
    raw_token = token.decode('utf-8') if isinstance(token, bytes) else token

    headers = {
        'Authorization': f'Bearer {raw_token}',
        'Accept': 'application/json',
    }
    resp = requests.get(url, headers=headers, timeout=3.0)
    resp.raise_for_status()
    return resp.json()



def get_or_create_remote_user(user_id, token):
    """
    Return a RemoteUser for this ID. If no local row exists, or if it's older
    than USER_CACHE_TTL, fetch from auth server and save.
    """
    try:
        user = RemoteUser.objects.get(id=user_id)
    except RemoteUser.DoesNotExist:
        user = None

    need_fetch = (user is None or (timezone.now() -
                  user.updated_at) > USER_CACHE_TTL)

    if need_fetch:
        data = fetch_user_from_auth_server(user_id, token)
        if not data:
            # Auth server couldn’t return a user → we give up (user stays None)
            return user
        data = data.get('data', {})

        # Map JSON from auth to your RemoteUser fields:
        avatar = data.get('avatar', {}) or {}
        defaults = {
            'id': user_id,
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'initials': data.get('initials', ''),
            'email': data.get('email', ''),
            'is_staff': data.get('is_staff', False),
            'is_active': data.get('is_active', True),
            'is_superuser': data.get('is_superuser', False),
            'start_date': data.get('start_date', None),
            'role': data.get('role', None),
            'permissions': data.get('permissions', {}),
            'avatar': data.get('avatar', None),
        }

        # Create or update the local mirror row:
        user, _ = RemoteUser.objects.update_or_create(
            id=user_id, defaults=defaults)

    return user
