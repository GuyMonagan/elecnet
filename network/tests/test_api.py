import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from network.models import BusinessUnit, Product
from datetime import date

from decimal import Decimal
from users.models import User


@pytest.mark.django_db
def test_debt_to_supplier_is_readonly():
    User = get_user_model()
    user = User.objects.create_user(
        email="staff@example.com",
        password="testpass123",
        is_active=True,
        is_staff=True
    )

    client = APIClient()
    response = client.post("/api/token/", data={
        "email": "staff@example.com",
        "password": "testpass123"
    })
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    supplier = BusinessUnit.objects.create(name="Поставщик", email="sup@ex.com", country="RU",
                                           city="Москва", street="Тверская", house_number="1")
    unit = BusinessUnit.objects.create(name="Клиент", email="cli@ex.com", country="RU",
                                       city="СПб", street="Невский", house_number="2", supplier=supplier)

    # Попробуем изменить задолженность через PATCH
    patch = client.patch(f"/api/units/{unit.id}/", data={"debt_to_supplier": "99999.99"}, format="json")

    unit.refresh_from_db()
    assert unit.debt_to_supplier == Decimal("0.00")
    assert patch.status_code in [200, 400]  # может быть 200, но поле проигнорировано


@pytest.mark.django_db
def test_filter_businessunits_by_country():
    user = User.objects.create_user(email="staff@example.com", password="testpass123", is_active=True, is_staff=True)
    client = APIClient()
    client.force_authenticate(user=user)

    # Создаём 2 юнита с разными странами
    france_unit = BusinessUnit.objects.create(
        name="ParisTech",
        email="paris@example.com",
        country="France",
        city="Paris",
        street="Rue Lafayette",
        house_number="12"
    )
    germany_unit = BusinessUnit.objects.create(
        name="BerlinStore",
        email="berlin@example.com",
        country="Germany",
        city="Berlin",
        street="Alexanderplatz",
        house_number="3"
    )

    response = client.get("/api/units/?search=France")
    assert response.status_code == 200
    names = [unit['name'] for unit in response.json()]
    assert france_unit.name in names
    assert germany_unit.name not in names


@pytest.mark.django_db
def test_create_product_for_businessunit():
    user = User.objects.create_user(email="product@admin.com", password="test1234", is_active=True, is_staff=True)
    client = APIClient()
    client.force_authenticate(user=user)

    unit = BusinessUnit.objects.create(
        name="TechStore",
        email="ts@example.com",
        country="USA",
        city="New York",
        street="Wall St",
        house_number="10"
    )

    payload = {
        "owner": unit.id,
        "name": "SmartFridge",
        "model": "XK-9000",
        "release_date": str(date.today())
    }

    response = client.post("/api/products/", payload, format="json")
    assert response.status_code == 201
    assert Product.objects.filter(name="SmartFridge", owner=unit).exists()
