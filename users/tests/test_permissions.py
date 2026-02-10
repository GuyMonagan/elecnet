import pytest
from rest_framework.test import APIClient
from users.models import User
from network.models import BusinessUnit


@pytest.mark.django_db
def test_non_staff_user_cannot_access_api():
    # создаём обычного пользователя
    user = User.objects.create_user(
        email="normie@example.com",
        password="test123",
        is_active=True,  # активный, но не staff
        is_staff=False
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/units/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_staff_user_can_access_api():
    staff_user = User.objects.create_user(
        email="admin@example.com",
        password="test123",
        is_active=True,
        is_staff=True
    )

    client = APIClient()
    client.force_authenticate(user=staff_user)

    response = client.get("/api/units/")
    assert response.status_code == 200
