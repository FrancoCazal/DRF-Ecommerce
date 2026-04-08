from django.conf import settings
from django.middleware.csrf import get_token
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users.api.serializers import RegisterSerializer, UserSerializer


def _set_auth_cookies(response, access, refresh):
    response.set_cookie(
        'access_token',
        str(access),
        max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
    )
    response.set_cookie(
        'refresh_token',
        str(refresh),
        max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        path='/api/v1/auth/',
    )


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class CookieLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            _set_auth_cookies(
                response,
                response.data['access'],
                response.data['refresh'],
            )
            csrf_token = get_token(request)
            response.data = {
                'detail': 'Login successful.',
                'csrftoken': csrf_token,
            }
        return response


class CookieRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Read refresh token from cookie if not in body
        if 'refresh' not in request.data:
            refresh = request.COOKIES.get('refresh_token')
            if refresh:
                if hasattr(request.data, '_mutable'):
                    request.data._mutable = True
                    request.data['refresh'] = refresh
                    request.data._mutable = False
                else:
                    request.data['refresh'] = refresh

        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            _set_auth_cookies(
                response,
                response.data['access'],
                response.data.get('refresh', request.data.get('refresh')),
            )
            response.data = {'detail': 'Token refreshed.'}
        return response


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token') or request.data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass

        response = Response({'detail': 'Logged out.'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token', path='/api/v1/auth/')
        return response


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
