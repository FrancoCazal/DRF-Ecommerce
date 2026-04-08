import pytest
from django.urls import reverse
from apps.users.models import User


@pytest.mark.django_db
class TestRegister:
    url = '/api/v1/auth/register/'

    def test_register_success(self, api_client):
        data = {
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'securepass123',
        }
        response = api_client.post(self.url, data)
        assert response.status_code == 201
        assert User.objects.filter(email='new@example.com').exists()

    def test_register_short_password(self, api_client):
        data = {
            'email': 'short@example.com',
            'first_name': 'Short',
            'last_name': 'Pass',
            'password': '123',
        }
        response = api_client.post(self.url, data)
        assert response.status_code == 400

    def test_register_duplicate_email(self, api_client, user):
        data = {
            'email': user.email,
            'first_name': 'Dup',
            'last_name': 'User',
            'password': 'securepass123',
        }
        response = api_client.post(self.url, data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestLogin:
    url = '/api/v1/auth/login/'

    def test_login_success(self, api_client, user):
        response = api_client.post(self.url, {
            'email': user.email,
            'password': 'testpass123',
        })
        assert response.status_code == 200
        assert 'access_token' in response.cookies

    def test_login_wrong_password(self, api_client, user):
        response = api_client.post(self.url, {
            'email': user.email,
            'password': 'wrongpass',
        })
        assert response.status_code == 401


@pytest.mark.django_db
class TestLogout:
    url = '/api/v1/auth/logout/'

    def test_logout_clears_cookies(self, auth_client):
        response = auth_client.post(self.url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestUserProfile:
    url = '/api/v1/auth/me/'

    def test_get_profile(self, auth_client, user):
        response = auth_client.get(self.url)
        assert response.status_code == 200
        assert response.data['email'] == user.email

    def test_update_profile(self, auth_client):
        response = auth_client.patch(self.url, {'first_name': 'Updated'})
        assert response.status_code == 200
        assert response.data['first_name'] == 'Updated'

    def test_unauthenticated_access(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 401
