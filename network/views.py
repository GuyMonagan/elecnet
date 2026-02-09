from rest_framework import viewsets, permissions, filters
from .models import BusinessUnit, Product
from .serializers import BusinessUnitSerializer, ProductSerializer
from users.permissions import IsActiveStaff


class BusinessUnitViewSet(viewsets.ModelViewSet):
    queryset = BusinessUnit.objects.all()
    serializer_class = BusinessUnitSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveStaff]
    filter_backends = [filters.SearchFilter]
    search_fields = ['country']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveStaff]
