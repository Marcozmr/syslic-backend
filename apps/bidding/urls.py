from django.urls import include, path
from rest_framework import routers

from .views import (
    TypeViewSet,
    ModalityViewSet,
    InterestViewSet,
    PlatformViewSet,
    PlatformListViewSet,
    PlatformLoginViewSet,
    PhaseViewSet,
    StatusViewSet,
    StatusBasicViewSet,
    DisputeViewSet,
    RequirementViewSet,
    BiddingListViewSet,
    BiddingListContractViewSet,
    BiddingViewSet,
    BiddingHomologatedViewSet,
    BiddingFiledViewSet,
    BiddingItemViewSet,
    BiddingItemResultViewSet,
    BiddingFilterViewSet,
    BiddingFileViewSet,
    BiddingImportedViewSet,
    BiddingImportedListView,
    BiddingImportedSimpleListView,
    BiddingHistoryViewSet,
    BiddingCompanyFileViewSet,
    BiddingCompanyCertificateViewSet,
    BiddingItemTypeConvertViewSet
)

app_name = 'bidding'

router = routers.DefaultRouter()
router.register(r'type', TypeViewSet, basename="Type")
router.register(r'modality', ModalityViewSet, basename="Modality")
router.register(r'interest', InterestViewSet, basename="Insterest")
router.register(r'platform/login', PlatformLoginViewSet, basename="PlatformLogin")
router.register(r'platform-list', PlatformListViewSet, basename="PlatformList")
router.register(r'platform', PlatformViewSet, basename="Platform")
router.register(r'dispute', DisputeViewSet, basename="Dispute")
router.register(r'requirement', RequirementViewSet, basename="Requirement")
router.register(r'phase', PhaseViewSet, basename="Phase")
router.register(r'status', StatusViewSet, basename="Status")
router.register(r'status-basic', StatusBasicViewSet, basename="StatusBasic")
router.register(r'item', BiddingItemViewSet, basename="Item")
router.register(r'item/type/convert', BiddingItemTypeConvertViewSet, basename="ItemTypeConvert")
router.register(r'item/result', BiddingItemResultViewSet, basename="ItemResult")
router.register(r'homologated', BiddingHomologatedViewSet, basename="Homologated")
router.register(r'filed', BiddingFiledViewSet, basename="Filed")
router.register(r'filter', BiddingFilterViewSet, basename="Filter")
router.register(r'attach/file', BiddingFileViewSet, basename="BiddingFile")
router.register(r'imported/simple', BiddingImportedSimpleListView, basename="BiddingImported")
router.register(r'imported', BiddingImportedListView, basename="BiddingImported")
router.register(r'company/certificate', BiddingCompanyCertificateViewSet, basename="BiddingCompanyCertificate")
router.register(r'company/file', BiddingCompanyFileViewSet, basename="BiddingCompanyFile")
router.register(r'history', BiddingHistoryViewSet, basename="BiddingHistory")
router.register(r'list/contract', BiddingListContractViewSet, basename="BiddingListContract")
router.register(r'list', BiddingListViewSet, basename="BiddingList")
router.register(r'', BiddingViewSet, basename="Bidding")

urlpatterns = [
    path('import/', BiddingImportedViewSet.as_view({
        'post': 'import_bidding',
    })),
    path('', include(router.urls)),
]
