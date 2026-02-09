from rest_framework import serializers
from .models import BusinessUnit, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BusinessUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnit
        exclude = ('debt_to_supplier',)  # нельзя изменять через API

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['debt_to_supplier'] = str(instance.debt_to_supplier)  # только read-only
        return data
