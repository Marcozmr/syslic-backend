from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from .models import (
    Client,
)

from .serializers import (
    ClientSerializer,
    ClientListSerialier,
)

from .pagination import (
    ClientPagination,
)

from .permissions import (
        HasModelPermission,
        HasOtherPermission,
)

class ClientViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ClientSerializer
    pagination_class = ClientPagination
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
        return Client.objects.all().order_by('pk')

class ClientListViewSet(ModelViewSet):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ClientListSerialier
    pagination_class = ClientPagination
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
        return Client.objects.all().order_by('pk')
