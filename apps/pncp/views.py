from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as django_filters
from django_filters import Filter

from .models import (
    HiringModalitie,
    Spheres,
    Powers,
    TypeCallingInstrument,
    PncpFilter,
)

from .serializers import (
    HiringModalitieSerializer,
    SpheresSerializer,
    PowersSerializer,
    TypeCallingInstrumentSerializer,
    PncpFilterSerializer,
)

from .pagination import (
    PncpPagination,
)

from apps.bidding.permissions import (
    HasModelPermission,
    HasModelSettingsPermission,
    HasOtherPermission,
)

class HiringModalitieViewSet(ModelViewSet):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = HiringModalitieSerializer
    pagination_class = PncpPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'nome',
        'codigo',
    ]

    def get_queryset(self):
        return HiringModalitie.objects.all().order_by('pk')

class SpheresViewSet(ModelViewSet):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = SpheresSerializer
    pagination_class = PncpPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'nome',
        'codigo',
    ]

    def get_queryset(self):
        return Spheres.objects.all().order_by('pk')

class PowersViewSet(ModelViewSet):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = PowersSerializer
    pagination_class = PncpPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'nome',
        'codigo',
    ]

    def get_queryset(self):
        return Powers.objects.all().order_by('pk')

class TypeCallingInstrumentViewSet(ModelViewSet):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = TypeCallingInstrumentSerializer
    pagination_class = PncpPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'nome',
        'codigo',
    ]

    def get_queryset(self):
        return TypeCallingInstrument.objects.all().order_by('pk')

class PncpFilterViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = PncpFilterSerializer
    pagination_class = PncpPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return PncpFilter.objects.all().order_by('pk')