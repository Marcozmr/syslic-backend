from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from apps.utils.cache import ModelViewSetCached

from .models import (
    Freight,
    Carrier,
)

from .serializers import (
    FreightSerializer,
    CarrierSerializer,
    CarrierListSerialier,
)

from .pagination import (
    TransportPagination,
)

from .permissions import (
    HasModelPermission,
    HasOtherPermission,
    HasModelSettingsPermission,
)

class FreightViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission | HasModelSettingsPermission,)
    serializer_class = FreightSerializer
    pagination_class = TransportPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'name',
        'value',
        ]

    def get_queryset(self):
        return Freight.objects.all().order_by('pk')

class CarrierViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = CarrierSerializer
    pagination_class = TransportPagination
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
        ]

    ordering_fields = [
        'id',
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
        ]

    def get_queryset(self):
        return Carrier.objects.all().order_by('pk')

class CarrierListViewSet(ModelViewSetCached):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = CarrierListSerialier
    pagination_class = TransportPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter]
    search_fields = [
        'id',
        'name',
        'name_fantasy',
        'cnpj',
        'email',
        'ie',
        'city__name',
        'state__name',
        'state__code',
        ]

    ordering_fields = [
        'id',
        'name',
        'name_fantasy',
        'cnpj',
        'email',
        'ie',        
        'phone_number',
        'city__name',
        'state__name',
        'state__code',
        ]

    def get_queryset(self):
        return Carrier.objects.all().order_by('pk')
