import pytest
from decimal import Decimal
from network.models import BusinessUnit, Product


@pytest.mark.django_db
def test_get_level_calculates_correct_depth():
    """
    Ensure hierarchy level is calculated correctly.
    """
    root = BusinessUnit.objects.create(
        name="Root", email="r@r.r", country="RU", city="М", street="У", house_number="1"
    )
    mid = BusinessUnit.objects.create(
        name="Mid",
        email="m@m.m",
        country="RU",
        city="М",
        street="У",
        house_number="2",
        supplier=root,
    )
    leaf = BusinessUnit.objects.create(
        name="Leaf",
        email="l@l.l",
        country="RU",
        city="М",
        street="У",
        house_number="3",
        supplier=mid,
    )

    assert root.get_level() == 0
    assert mid.get_level() == 1
    assert leaf.get_level() == 2


@pytest.mark.django_db
def test_str_methods_return_readable_names():
    """
    Ensure __str__ methods return readable representations.
    """
    unit = BusinessUnit.objects.create(
        name="Node",
        email="n@n.n",
        country="RU",
        city="Москва",
        street="Улица",
        house_number="10",
    )
    product = Product.objects.create(
        name="TV", model="X9000", release_date="2022-01-01", owner=unit
    )

    assert str(unit) == "Node — Москва"
    assert str(product) == "TV (X9000)"


@pytest.mark.django_db
def test_businessunit_supplier_relationship():
    """
    Ensure supplier relationship is stored correctly.
    """

    parent = BusinessUnit.objects.create(
        name="Parent",
        email="parent@example.com",
        country="RU",
        city="Moscow",
        street="Tverskaya",
        house_number="1",
    )

    child = BusinessUnit.objects.create(
        name="Child",
        email="child@example.com",
        country="RU",
        city="SPb",
        street="Nevsky",
        house_number="2",
        supplier=parent,
    )

    assert child.supplier == parent
    assert parent.clients.count() == 1
    assert parent.clients.first() == child

@pytest.mark.django_db
def test_debt_defaults_to_zero():
    """
    Ensure debt_to_supplier defaults to 0.00.
    """
    unit = BusinessUnit.objects.create(
        name="Test Unit",
        email="unit@example.com",
        country="RU",
        city="Moscow",
        street="Tverskaya",
        house_number="1",
    )

    assert unit.debt_to_supplier == Decimal("0.00")
