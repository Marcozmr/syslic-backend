from django.urls import include, path
from rest_framework import routers

from .views import (
   FreightViewSet,
   CarrierViewSet,
   CarrierListViewSet,
)

app_name = 'transport'

router = routers.DefaultRouter()
router.register(r'freight', FreightViewSet, basename="Freight")
router.register(r'list', CarrierListViewSet, basename="TransportList")
router.register(r'', CarrierViewSet, basename="Transport")

urlpatterns = [
    path('', include(router.urls)),
]
