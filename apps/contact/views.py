from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as django_filters
from django_filters import FilterSet

from .models import (
    Contact,
)

from .serializers import (
    ContactSerializer,
)

from .pagination import (
    ContactPagination,
)

from .permissions import (
    HasModelPermission,
)

class ContactFilter(FilterSet):
    class Meta:
        model = Contact
        fields = {
            'id': ['exact'],
            'name': ['exact'],
            'email': ['exact'],
            'phone_number': ['exact'],
            'address': ['exact'],
            'address_type': ['exact'],
            'neighborhood': ['exact'],
            'neighborhood_type': ['exact'],
            'complement': ['exact'],
            'number': ['exact'],
            'city': ['exact'],
            'state': ['exact'],
            'country': ['exact'],
            'zip_code': ['exact'],
            'position': ['exact'],
            'sector': ['exact'],
            'company': ['exact'],
            'client': ['exact'],
            'supplier': ['exact'],
            'carrier': ['exact'],
        }

class ContactViewSet(ModelViewSet):
    permission_classes = (HasModelPermission,)
    serializer_class = ContactSerializer
    pagination_class = ContactPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'name',
        'email',
        'phone_number',
        'address',
        'address_type__name',
        'neighborhood',
        'neighborhood_type__name',
        'complement',
        'number',
        'city__name',
        'state__name',
        'country__name',
        'zip_code',
        'position',
        'sector',
        'company__name',
        'client__name',
        'supplier__name',
    ]

    ordering_fields = [
        'id',
        'name',
        'email',
        'phone_number',
        'address',
        'address_type__name',
        'neighborhood',
        'neighborhood_type__name',
        'complement',
        'number',
        'city__name',
        'state__name',
        'country__name',
        'zip_code',
        'position',
        'sector',
        'company__name',
        'client__name',
        'supplier__name',
    ]

    filter_class = ContactFilter

    def get_queryset(self):
        return Contact.objects.all().order_by('pk')
