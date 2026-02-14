from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from network.models import BusinessUnit, Product
from users.models import User


@pytest.mark.django_db
def test_debt_to_supplier_is_read_only():
    """
    Ensure debt_to_supplier cannot be modified via API.
    """

    User = get_user_model()
    user = User.objects.create_user(
        email="staff@example.com",
        password="testpass123",
        is_active=True,
        is_staff=True,
    )

    client = APIClient()
    client.force_authenticate(user=user)

    supplier = BusinessUnit.objects.create(
        name="Supplier",
        email="sup@example.com",
        country="RU",
        city="Moscow",
        street="Tverskaya",
        house_number="1",
    )

    unit = BusinessUnit.objects.create(
        name="Client",
        email="cli@example.com",
        country="RU",
        city="SPb",
        street="Nevsky",
        house_number="2",
        supplier=supplier,
        debt_to_supplier=Decimal("0.00"),
    )

    response = client.patch(
        f"/api/units/{unit.id}/",
        {"debt_to_supplier": "99999.99"},
        format="json",
    )

    unit.refresh_from_db()

    assert response.status_code == 200
    assert unit.debt_to_supplier == Decimal("0.00")
    assert response.data["debt_to_supplier"] == "0.00"


@pytest.mark.django_db
def test_create_product_for_businessunit():
    """
    Verify that a product can be created for a business unit.
    """
    user = User.objects.create_user(
        email="product@admin.com", password="test1234", is_active=True, is_staff=True
    )
    client = APIClient()
    client.force_authenticate(user=user)

    unit = BusinessUnit.objects.create(
        name="TechStore",
        email="ts@example.com",
        country="USA",
        city="New York",
        street="Wall St",
        house_number="10",
    )

    payload = {
        "owner": unit.id,
        "name": "SmartFridge",
        "model": "XK-9000",
        "release_date": str(date.today()),
    }

    response = client.post("/api/products/", payload, format="json")
    assert response.status_code == 201
    assert Product.objects.filter(name="SmartFridge", owner=unit).exists()


@pytest.mark.django_db
def test_filter_businessunit_by_country():
    """
    Ensure business units can be filtered by country using query parameters.
    """

    user = User.objects.create_user(
        email="filter@example.com",
        password="test123",
        is_active=True,
        is_staff=True,
    )

    client = APIClient()
    client.force_authenticate(user=user)

    BusinessUnit.objects.create(
        name="Alpha",
        email="alpha@example.com",
        country="France",
        city="Paris",
        street="Rue Morgue",
        house_number="13",
    )

    BusinessUnit.objects.create(
        name="Beta",
        email="beta@example.com",
        country="Germany",
        city="Berlin",
        street="Kantstraße",
        house_number="42",
    )

    response = client.get("/api/units/?country=France")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["country"] == "France"
