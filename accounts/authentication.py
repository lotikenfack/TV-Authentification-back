from rest_framework.authentication import BaseAuthentication
from .models import AccessKey
from rest_framework import exceptions

class AccessKeyTokenAuthentication(BaseAuthentication):
    """
    Custom authentication for AccessKey using a token in the header: 'X-AccessKey-Token'.
    """
    def authenticate(self, request):
        token = request.headers.get('X-AccessKey-Token')
        if not token:
            return None
        try:
            access_key = AccessKey.objects.get(password=token, is_active=True)
        except AccessKey.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid or inactive AccessKey token')
        return (access_key, None)
