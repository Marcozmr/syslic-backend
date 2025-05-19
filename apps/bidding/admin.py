from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin

from .models import (
    BiddingType,
    Modality,
    Interest,
    Platform,
    PlatformLogin,
    Phase,
    Status,
    Dispute,
    Requirement,
    Bidding,
    BiddingItem,
    BiddingItemCompound,
    BiddingFilter,
    BiddingFile,
    BiddingImported,
    BiddingCompanyFile,
    BiddingCompanyCertificate,
)

@admin.register(
    BiddingType,
    Modality,
    Interest,
    Platform,
    PlatformLogin,
    Phase,
    Status,
    Dispute,
    Requirement,
    Bidding,
    BiddingItem,
    BiddingItemCompound,
    BiddingFilter,
    BiddingFile,
    BiddingImported,
    BiddingCompanyFile,
    BiddingCompanyCertificate,
)

class UniversalAdmin(ImportExportMixin, SimpleHistoryAdmin, admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
