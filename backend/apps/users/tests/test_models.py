import pytest
from apps.users.models import User


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            email='john@example.com',
            first_name='John',
            last_name='Doe',
            password='securepass123',
        )
        assert user.email == 'john@example.com'
        assert user.first_name == 'John'
        assert user.check_password('securepass123')
        assert not user.is_staff
        assert not user.is_superuser
        assert user.is_active

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='adminpass123',
        )
        assert admin.is_staff
        assert admin.is_superuser

    def test_create_user_without_email_raises(self):
        with pytest.raises(ValueError, match='email'):
            User.objects.create_user(
                email='',
                first_name='No',
                last_name='Email',
                password='pass123',
            )

    def test_email_is_normalized(self):
        user = User.objects.create_user(
            email='Test@EXAMPLE.COM',
            first_name='Test',
            last_name='User',
            password='pass123',
        )
        assert user.email == 'Test@example.com'

    def test_full_name(self):
        user = User(first_name='John', last_name='Doe')
        assert user.full_name == 'John Doe'

    def test_str_returns_email(self):
        user = User(email='str@example.com')
        assert str(user) == 'str@example.com'
