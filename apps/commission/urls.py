from django.urls import include, path
from rest_framework import routers
from .views import (
    CommissionViewSet,
    OrderInvoicingIsDoneViewSet,
    CommissionUserValuesViewSet,
)

app_name = 'commission'

router = routers.DefaultRouter()
router.register(r'commission/total/from/user', CommissionUserValuesViewSet, basename="CommissionUserValues")
router.register(r'commission/from/invoicing', OrderInvoicingIsDoneViewSet, basename="OrderInvoicingIsDone")
router.register(r'commission', CommissionViewSet, basename="Commission")

urlpatterns = [
    path('', include(router.urls)),
]
