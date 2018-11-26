from rest_framework import authentication


class JWTAuthentication(authentication.BaseAuthentication):
    key = 'Token'

    def authenticate(self, request):
        return {}
