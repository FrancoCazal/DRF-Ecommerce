from django.urls import path
from apps.users.api.views import (
    RegisterView,
    CookieLoginView,
    CookieRefreshView,
    LogoutView,
    UserProfileView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CookieLoginView.as_view(), name='login'),
    path('refresh/', CookieRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserProfileView.as_view(), name='user_profile'),
]
