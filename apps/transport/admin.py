from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import (
    Freight,
    Carrier,
)


class FreightAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name','value']
    search_fields = ['name']

class CarrierAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name','name_fantasy', 'cnpj', 'ie']
    search_fields = ['name', 'cnpj']

admin.site.register(Freight, FreightAdmin)
admin.site.register(Carrier, CarrierAdmin)
