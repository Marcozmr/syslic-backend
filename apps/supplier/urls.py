from django.urls import include, path
from rest_framework import routers

from .views import (
   SupplierViewSet,
   SupplierListViewSet,
   CategoryViewSet,
)

app_name = 'supplier'

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet, basename="Category")
router.register(r'list', SupplierListViewSet, basename="SupplierList")
router.register(r'', SupplierViewSet, basename="Supplier")

urlpatterns = [
    path('', include(router.urls)),
]
