from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin

from .models import (
    Contract,
    ContractType,
    ContractScope,
    ContractStatus,
    ContractFile,
    ContractItem,
    ContractItemCompound,
)

@admin.register(
    Contract,
    ContractType,
    ContractScope,
    ContractStatus,
    ContractFile,
    ContractItem,
    ContractItemCompound,
)

class UniversalAdmin(ImportExportMixin, SimpleHistoryAdmin, admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
