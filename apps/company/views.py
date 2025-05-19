from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as django_filters

from apps.utils.cache import ModelViewSetCached

from .models import (
    Company,
    CompanyFile,
    CompanyCertificateStatus,
    CompanyCertificateFile,
    CompanyCertificate,
)
from .serializers import (
    CompanySerializer,
    CompanyFileSerializer,
    CompanyFileDetailSerializer,
    CompanyCertificateStatusSerializer,
    CompanyCertificateFileSerializer,
    CompanyCertificateSerializer,
    CompanyListSerializer,
)
from .pagination import CompanyPagination
from .permissions import (
        HasModelPermission,
        HasOtherPermission,
        HasUpdateCompanyPermission
)

class CompanyViewSet(ModelViewSetCached):
    serializer_class = CompanySerializer
    permission_classes = (HasModelPermission | HasOtherPermission,)
    pagination_class = CompanyPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter]
    search_fields = [
        'corporate_name',
        'name_fantasy',
        'cnpj',
        'ie',
        'email',
        'phone_number',
        'address',
        'neighborhood',
        'complement',
        'number',
        'city__name',
        'state__name',
        'state__code',
        'country__name',
        'zip_code',
        'margin_min',
        'tax_aliquot',
        'fixed_cost',
        ]

    ordering_fields = [
        'corporate_name',
        'name_fantasy',
        'cnpj',
        'ie',
        'email',
        'phone_number',
        'address',
        'neighborhood',
        'complement',
        'number',
        'city__name',
        'state__name',
        'state__code',
        'country__name',
        'zip_code',
        'margin_min',
        'tax_aliquot',
        'fixed_cost',
        ]

    def get_queryset(self):
        return Company.objects.all().order_by('corporate_name')

class CompanyListViewSet(ModelViewSetCached):
    http_method_names = ['get', 'options', 'head']
    serializer_class = CompanyListSerializer
    permission_classes = (HasModelPermission | HasOtherPermission,)
    pagination_class = CompanyPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter]
    search_fields = [
        'id',
        'corporate_name',
        'name_fantasy',
        'cnpj',
        'ie',
        'phone_number',
    ]

    ordering_fields = [
        'id',
        'corporate_name',
        'name_fantasy',
        'cnpj',
        'ie',
        'phone_number',
    ]

    def get_queryset(self):
        return Company.objects.all().order_by('pk')

class CompanyFileViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission | HasUpdateCompanyPermission,)
    serializer_class = CompanyFileSerializer

    cache_related_model_classes = [
            Company,
    ]

    def get_queryset(self):
        return CompanyFile.objects.all().order_by('pk')

class CompanyFileDetailViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = CompanyFileDetailSerializer
    pagination_class = CompanyPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'company__corporate_name',
        'document_name',
        'annotation',
        'link_certificates',
    ]

    ordering_fields = [
        'company__corporate_name',
        'document_name',
        'annotation',
        'link_certificates',
    ]

    filter_fields = {
        'company': ['exact'],
    }

    cache_related_model_classes = [
        Company,
    ]

    def get_queryset(self):
        return CompanyFile.objects.all().order_by('pk')

class CompanyCertificateStatusViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = CompanyCertificateStatusSerializer
    pagination_class = CompanyPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return CompanyCertificateStatus.objects.all().order_by('pk')

class CompanyCertificateFileViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission | HasUpdateCompanyPermission,)
    serializer_class = CompanyCertificateFileSerializer
    pagination_class = CompanyPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'file_name',
        'certificate',
    ]

    cache_related_model_classes = [
        Company,
    ]

    def get_queryset(self):
        return CompanyCertificateFile.objects.all().order_by('pk')

class CompanyCertificateViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission | HasUpdateCompanyPermission,)    
    serializer_class = CompanyCertificateSerializer
    pagination_class = CompanyPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]    

    search_fields = [
        'company__corporate_name',
        'client__name',
        'status__name',
        'end_authentication',
        'annotation',
    ]

    ordering_fields = [
        'company__corporate_name',
        'client__name',
        'status__name',
        'end_authentication',
        'annotation',
    ]

    filter_fields = {
        'company': ['exact'],
    }

    cache_related_model_classes = [
        Company,
    ]

    def get_queryset(self):
        return CompanyCertificate.objects.select_related('company',
                                                         'client',
                                                         'status',)
