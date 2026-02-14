import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.mark.django_db
def test_non_staff_user_cannot_access_api():
    """
    Ensure non-staff users cannot access protected API endpoints.
    """
    # создаём обычного пользователя
    user = User.objects.create_user(
        email="normie@example.com",
        password="dummy",
        is_active=True,  # активный, но не staff
        is_staff=False,
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/units/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_staff_user_can_access_api():
    """
    Ensure active staff users can access protected API endpoints.
    """
    staff_user = User.objects.create_user(
        email="admin@example.com", password="dummy", is_active=True, is_staff=True
    )

    client = APIClient()
    client.force_authenticate(user=staff_user)

    response = client.get("/api/units/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_inactive_staff_user_cannot_access_api():
    """
    Ensure inactive staff users cannot access protected API endpoints.
    """
    user = User.objects.create_user(
        email="ghost@example.com",
        password="dummy",
        is_active=False,
        is_staff=True,
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/units/")
    assert response.status_code == 403
