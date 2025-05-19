from django.urls import include, path
from rest_framework import routers

from .views import (
    OrderViewSet,
    OrderListViewSet,
    OrderInterestViewSet,
    OrderFileViewSet,
    OrderCommitmentStatusViewSet,
    OrderCommitmentViewSet,
    OrderCommitmentItemViewSet,
    OrderCommitmentItemProductViewSet,
    OrderItemsToCommitmentViewSet,
    OrderCommitmentFilterViewSet,
    OrderCommitmentFileViewSet,
    OrderCommitmentSituationViewSet,
    OrderFilterViewSet,
    OrderItemsReportViewSet,
    OrderDeliveryStatusViewSet,
    OrderDeliveryViewSet,
    OrderDeliveryFilterViewSet,
    OrderDeliveryItemViewSet,
    OrderDeliveryFileViewSet,
    OrderItemsToDeliveryViewSet,
    OrderDeliveryFreightCotationViewSet,
    OrderHistoryViewSet,
    OrderCommitmentHistoryViewSet,
    OrderDeliveryHistoryViewSet,
    OrderAssistanceViewSet,
    OrderAssistanceListViewSet,
    OrderAssistanceBasicViewSet,
    OrderToAssistanceViewSet,
    OrderAssistanceStatusViewSet,
    OrderAssistanceTypeViewSet,
    OrderAssistanceFilterViewSet,
    OrderProductsViewSet,
    OrderAuditPercentageAPIView,
    OrderDeliverySituationViewSet,
    OrderInvoicingStatusViewSet,
    OrderInvoicingFileViewSet,
    OrderInvoicingViewSet,
    OrderInvoicingListViewSet,
    OrderInvoicingViewViewSet,
    OrderInvoicingCreateViewSet,
    OrderDeliveryHasInvoicingViewSet,
    OrderInvoicingSituationViewSet,
    OrderInvoicingItemsViewSet,
    OrderInvoicingFilterViewSet,
    OrderCommitmentListViewSet,
    OrderDeliveryListViewSet,
)

app_name = 'order'

router = routers.DefaultRouter()
router.register(r'assistance/type', OrderAssistanceTypeViewSet, basename="OrderAssistanceType")
router.register(r'assistance/status', OrderAssistanceStatusViewSet, basename="OrderAssistanceStatus")
router.register(r'assistance/filter', OrderAssistanceFilterViewSet, basename="OrderAssistanceFilter")
router.register(r'assistance', OrderAssistanceViewSet, basename="OrderAssistance")
router.register(r'assistance-list', OrderAssistanceListViewSet, basename="OrderAssistanceList")
router.register(r'assistance-basic', OrderAssistanceBasicViewSet, basename="OrderAssistanceBasic")
router.register(r'assistance-order', OrderToAssistanceViewSet, basename="OrderToAssistance")
router.register(r'interest', OrderInterestViewSet, basename="OrderInsterest")
router.register(r'filter', OrderFilterViewSet, basename="OrderFilter")
router.register(r'attach/file', OrderFileViewSet, basename="OrderFile")
router.register(r'products', OrderProductsViewSet, basename="OrderProducts")
router.register(r'history', OrderHistoryViewSet, basename="OrderHistory")
router.register(r'commitment/status', OrderCommitmentStatusViewSet, basename="OrderCommitmentStatus")
router.register(r'commitment/filter', OrderCommitmentFilterViewSet, basename="OrderCommitmentFilter")
router.register(r'commitment/attach/file', OrderCommitmentFileViewSet, basename="OrderCommitmentFile")
router.register(r'commitment/item/product', OrderCommitmentItemProductViewSet, basename="OrderCommitmentItemProduct")
router.register(r'commitment/item', OrderCommitmentItemViewSet, basename="OrderCommitmentItem")
router.register(r'commitment/situation', OrderCommitmentSituationViewSet, basename="OrderCommitmentSituation")
router.register(r'commitment/history', OrderCommitmentHistoryViewSet, basename="OrderCommitmentHistory")
router.register(r'commitment/list', OrderCommitmentListViewSet, basename="OrderCommitmentList")
router.register(r'commitment', OrderCommitmentViewSet, basename="OrderCommitment")
router.register('items/to/commitment', OrderItemsToCommitmentViewSet, basename='OrderItemsToCommitment'),
router.register('items/to/delivery', OrderItemsToDeliveryViewSet, basename='OrderItemsToDelivery'),
router.register('items/report', OrderItemsReportViewSet, basename='OrderItemsReport'),
router.register(r'delivery/situation', OrderDeliverySituationViewSet, basename="OrderDeliverySituation"),
router.register(r'delivery/status', OrderDeliveryStatusViewSet, basename="OrderDeliveryStatus")
router.register(r'delivery/item', OrderDeliveryItemViewSet, basename="OrderDeliveryItem")
router.register(r'delivery/attach/file', OrderDeliveryFileViewSet, basename="OrderDeliveryFile")
router.register(r'delivery/freight', OrderDeliveryFreightCotationViewSet, basename="OrderDeliveryFreightCotation")
router.register(r'delivery/filter', OrderDeliveryFilterViewSet, basename="OrderDeliveryFilter")
router.register(r'delivery/history', OrderDeliveryHistoryViewSet, basename="OrderDeliveryHistory")
router.register(r'delivery/list', OrderDeliveryListViewSet, basename="OrderDeliveryList")
router.register(r'delivery', OrderDeliveryViewSet, basename="OrderDelivery")
router.register(r'invoicing/status', OrderInvoicingStatusViewSet, basename="OrderInvoicingStatus")
router.register(r'invoicing/attach/file', OrderInvoicingFileViewSet, basename="OrderInvoicingFile")
router.register(r'invoicing/create', OrderInvoicingCreateViewSet, basename="OrderInvoicingCreate")
router.register(r'invoicing/situation', OrderInvoicingSituationViewSet, basename="OrderInvoicingSituation")
router.register(r'invoicing/filter', OrderInvoicingFilterViewSet, basename="OrderInvoicingFilter")
router.register(r'invoicing/items', OrderInvoicingItemsViewSet, basename="OrderInvoicingItems")
router.register(r'invoicing-list', OrderInvoicingListViewSet, basename="OrderInvoicingList")
router.register(r'invoicing-view', OrderInvoicingViewViewSet, basename="OrderInvoicingView")
router.register(r'invoicing', OrderInvoicingViewSet, basename="OrderInvoicing")
router.register(r'list', OrderListViewSet, basename="OrderList")
router.register(r'', OrderViewSet, basename="Order")

urlpatterns = [
    path('', include(router.urls)),
    path('audit/percentage/', OrderAuditPercentageAPIView.as_view(), name='OrderAuditPercentage'),
    path('delivery/has-invoicing/<int:delivery_id>/', OrderDeliveryHasInvoicingViewSet.as_view(), name='OrderDeliveryHasInvoicing'),
]
