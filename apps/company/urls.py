from django.urls import include, path
from rest_framework import routers

from .views import (
    CompanyViewSet,
    CompanyFileViewSet,
    CompanyFileDetailViewSet,
    CompanyCertificateStatusViewSet,
    CompanyCertificateFileViewSet,
    CompanyCertificateViewSet,
    CompanyListViewSet,
)

app_name = 'company'

router = routers.DefaultRouter()
router.register(r'attach/file/detail', CompanyFileDetailViewSet, basename="CompanyFileDetail")
router.register(r'attach/file', CompanyFileViewSet, basename="CompanyFile")
router.register(r'certificate/status', CompanyCertificateStatusViewSet, basename="CompanyCertificateStatus")
router.register(r'certificate/file', CompanyCertificateFileViewSet, basename="CompanyCertificateFile")
router.register(r'certificate', CompanyCertificateViewSet, basename="CompanyCertificate")
router.register(r'company-list', CompanyListViewSet, basename="CompanyList")
router.register(r'', CompanyViewSet, basename="Company")

urlpatterns = [
    path('', include(router.urls)),
]
