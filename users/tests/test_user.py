import pytest

from users.models import User


@pytest.mark.django_db
def test_user_manager_creates_user_and_superuser():
    """
    Verify that UserManager correctly creates regular users and superusers
    with appropriate permission flags.
    """
    user = User.objects.create_user(email="simple@ex.com", password="test123")
    assert user.email == "simple@ex.com"
    assert user.is_staff is False

    superuser = User.objects.create_superuser(email="boss@ex.com", password="admin123")
    assert superuser.is_superuser is True
    assert superuser.is_staff is True
