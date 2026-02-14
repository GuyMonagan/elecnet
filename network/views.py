from rest_framework import filters, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from users.permissions import IsActiveStaff

from .models import BusinessUnit, Product
from .serializers import BusinessUnitSerializer, ProductSerializer


class BusinessUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing business units.
    Accessible only to active staff users.
    """

    queryset = BusinessUnit.objects.all()
    serializer_class = BusinessUnitSerializer
    permission_classes = [IsActiveStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing products.
    Accessible only to active staff users.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveStaff]
