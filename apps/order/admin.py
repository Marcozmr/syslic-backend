from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin

from .models import (
    Order,
    OrderInterest,
    OrderFilter,
    OrderFile,
    OrderCommitmentStatus,
    OrderCommitment,
    OrderCommitmentItem,
    OrderCommitmentItemProduct,
    OrderCommitmentFilter,
    OrderCommitmentFile,
    OrderDeliveryStatus,
    OrderDelivery,
    OrderDeliveryFilter,
    OrderDeliveryItem,
    OrderDeliveryFile,
    OrderDeliveryFreightCotation,
    OrderAssistance,
    OrderAssistanceStatus,
    OrderAssistanceType,
    OrderAssistanceFilter,
    OrderAuditPercentage,
    OrderInvoicingStatus,
    OrderInvoicingFile,
    OrderInvoicing,
)

@admin.register(
    Order,
    OrderInterest,
    OrderFilter,
    OrderFile,
    OrderCommitmentStatus,
    OrderCommitment,
    OrderCommitmentItem,
    OrderCommitmentItemProduct,
    OrderCommitmentFilter,
    OrderCommitmentFile,
    OrderDeliveryStatus,
    OrderDelivery,
    OrderDeliveryFilter,
    OrderDeliveryItem,
    OrderDeliveryFile,
    OrderDeliveryFreightCotation,
    OrderAssistance,
    OrderAssistanceStatus,
    OrderAssistanceType,
    OrderAssistanceFilter,
    OrderAuditPercentage,
    OrderInvoicingStatus,
    OrderInvoicingFile,
    OrderInvoicing,
)

class UniversalAdmin(ImportExportMixin, SimpleHistoryAdmin, admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
