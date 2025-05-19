from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import Client


class ClientAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name','name_fantasy', 'cnpj', 'ie']
    search_fields = ['name', 'cnpj']

admin.site.register(Client, ClientAdmin)
