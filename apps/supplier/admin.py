from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import (
    Category,
    Supplier,
)

class CategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class SupplierAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name','name_fantasy', 'cnpj', 'ie']
    search_fields = ['name', 'cnpj']

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Category, CategoryAdmin)
