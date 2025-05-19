from import_export.admin import ImportExportMixin
from django.contrib import admin

from .models import (
    HiringModalitie,
    Spheres,
    Powers,
    TypeCallingInstrument,
    PncpFilter,
)

@admin.register(
    HiringModalitie,
    Spheres,
    Powers,
    TypeCallingInstrument,
    PncpFilter,
)

class UniversalAdmin(ImportExportMixin, admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
