from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import (
    Contact,
)

class ContactAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name','phone_number', 'sector', 'position']
    search_fields = ['name','phone_number', 'sector', 'position']

admin.site.register(Contact, ContactAdmin)
