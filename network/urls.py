from rest_framework.routers import DefaultRouter
from .views import BusinessUnitViewSet, ProductViewSet

router = DefaultRouter()
router.register('units', BusinessUnitViewSet)
router.register('products', ProductViewSet)

urlpatterns = router.urls
