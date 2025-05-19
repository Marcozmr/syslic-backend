from rest_framework import filters

from apps.utils.cache import ModelViewSetCached

from .models import (
    Supplier,
    Category,
)

from .serializers import (
    SupplierSerializer,
    SupplierListSerializer,
    CategorySerializer,
)

from .pagination import (
    SupplierPagination,
)

from .permissions import (
        HasModelPermission,
        HasModelSettingsPermission,
        HasOtherPermission,
)

class CategoryViewSet(ModelViewSetCached):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = CategorySerializer
    pagination_class = SupplierPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'name',
    ]

    def get_queryset(self):
        return Category.objects.all().order_by('pk')

class SupplierViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = SupplierSerializer
    pagination_class = SupplierPagination    
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter]

    search_fields = [
        'name',
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
        'pix_key',
        'account_owner',
        'bank_name',
        'bank_agency',
        'bank_account',
        'category__name',
        ]

    ordering_fields = [
        'name',
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
        'pix_key',
        'account_owner',
        'bank_name',
        'bank_agency',
        'bank_account',
        ]

    def get_queryset(self):
        return Supplier.objects.all().order_by('pk')

class SupplierListViewSet(ModelViewSetCached):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = SupplierListSerializer
    pagination_class = SupplierPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter]

    search_fields = [
        'id',
        'name',
        'name_fantasy',
        'cnpj',
        'phone_number',
        'city__name',
        'state__name',
        'state__code',
        'category__name',
    ]

    ordering_fields = [
        'id',
        'name',
        'name_fantasy',
        'cnpj',        
        'phone_number',
        'city__name',
        'state__name',
        'state__code',
        'category__name',
    ]

    def get_queryset(self):
        return Supplier.objects.all().order_by('pk')