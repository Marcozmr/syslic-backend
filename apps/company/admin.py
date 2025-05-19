from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import (
    Company,
    CompanyFile,
    CompanyCertificateStatus,
    CompanyCertificateFile,
    CompanyCertificate,
)

class CompanyAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['corporate_name','name_fantasy', 'cnpj', 'ie']
    search_fields = ['corporate_name', 'cnpj']

class CompanyFileAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [
            'file_name',
            'document_name',
            'annotation',
            'file',
            'date_emission',
            'date_validity',
            'link_certificates',
            'company',
        ]

class CompanyCertificateAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [
            'annotation',
            'status',
            'client',
            'end_authentication',
            'company',
        ]

class CompanyCertificateFileAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [
            'file',
            'file_name',
            'certificate',
        ]

class CompanyCertificateStatusAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name','color']
    search_fields = ['name']

admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyFile, CompanyFileAdmin)
admin.site.register(CompanyCertificate, CompanyCertificateAdmin)
admin.site.register(CompanyCertificateFile, CompanyCertificateFileAdmin)
admin.site.register(CompanyCertificateStatus, CompanyCertificateStatusAdmin)

