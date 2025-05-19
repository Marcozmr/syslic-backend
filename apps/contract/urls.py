from django.urls import include, path
from rest_framework import routers

from .views import (
    ContractTypeViewSet,
    ContractScopeViewSet,
    ContractStatusViewSet,
    ContractViewSet,
    ContractItemViewSet,
    ContractFileViewSet,
    ContractItemsToCommitmentViewSet,
    ContractFilterViewSet,
    ContractHistoryViewSet,
    ContractListViewSet,
)

app_name = 'contract'

router = routers.DefaultRouter()
router.register(r'type', ContractTypeViewSet, basename="ContractType")
router.register(r'scope', ContractScopeViewSet, basename="ContractScope")
router.register(r'status', ContractStatusViewSet, basename="ContractStatus")
router.register(r'item', ContractItemViewSet, basename="ContractItem")
router.register(r'filter', ContractFilterViewSet, basename="Filter")
router.register(r'attach/file', ContractFileViewSet, basename="ContractFile")
router.register(r'items/to/commitment', ContractItemsToCommitmentViewSet, basename='ContractItemsToCommitment'),
router.register(r'history', ContractHistoryViewSet, basename="ContractHistory")
router.register(r'list', ContractListViewSet, basename="ContractList")
router.register(r'', ContractViewSet, basename="Contract")

urlpatterns = [
    path('', include(router.urls)),
]
