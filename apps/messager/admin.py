from import_export.admin import ImportExportMixin
from django.contrib import admin

from .models import (
    Message,
    MessageVisualization,
)

@admin.register(
    Message,
    MessageVisualization,
)

class UniversalAdmin(ImportExportMixin, admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
