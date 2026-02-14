from rest_framework import serializers

from .models import BusinessUnit, Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    """
    class Meta:
        model = Product
        fields = "__all__"


class BusinessUnitSerializer(serializers.ModelSerializer):
    """
    Serializer for BusinessUnit model.
    Debt field is read-only via API.
    """
    debt_to_supplier = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = BusinessUnit
        fields = "__all__"
