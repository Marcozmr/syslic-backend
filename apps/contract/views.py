from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as django_filters
from django_filters import FilterSet
from django_filters import Filter

from apps.utils.cache import ModelViewSetCached

from .models import (
    Contract,
    ContractType,
    ContractScope,
    ContractStatus,
    ContractFile,
    ContractItem,
    ContractFilter,
)

from .serializers import (
    ContractSerializer,
    ContractTypeSerializer,
    ContractScopeSerializer,
    ContractStatusSerializer,
    ContractFileSerializer,
    ContractItemSerializer,
    ContractItemsToCommitmentSerializer,
    ContractFilterSerializer,
    ContractHistorySerializer,
    ContractListSerializer,
)

from .pagination import (
    ContractPagination,
)

from .permissions import (
    HasModelPermission,
    HasModelSettingsPermission,
    HasOtherPermission,
)

class ContractTypeViewSet(ModelViewSetCached):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = ContractTypeSerializer
    pagination_class = ContractPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'name',
    ]

    ordering_fields = [
        'id',
        'name',
    ]

    ordering = ['name']

    filter_fields = {
        'name': ['exact'],
    }

    def get_queryset(self):
        return ContractType.objects.all().order_by('pk')

class ContractScopeViewSet(ModelViewSetCached):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = ContractScopeSerializer
    pagination_class = ContractPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'name',
    ]

    ordering_fields = [
        'id',
        'name',
    ]

    ordering = ['name']

    filter_fields = {
        'name': ['exact'],
    }

    def get_queryset(self):
        return ContractScope.objects.all().order_by('pk')

class ContractStatusViewFilter(FilterSet):
    initial = django_filters.BooleanFilter(field_name='initial')

    class Meta:
        model = ContractStatus
        fields = ['initial']

class ContractStatusViewSet(ModelViewSetCached):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = ContractStatusSerializer
    pagination_class = ContractPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'name',
    ]

    ordering_fields = [
        'id',
        'name',
    ]

    ordering = ['name']

    filter_fields = {
        'name': ['exact'],
    }

    filter_class = ContractStatusViewFilter

    def get_queryset(self):
        return ContractStatus.objects.all().order_by('pk')

class ContractFileViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ContractFileSerializer

    def get_queryset(self):
        return ContractFile.objects.all().order_by('pk')

class ContractViewFieldsFilter(Filter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(**{self.field_name: value})
        return qs

class ContractViewFilter(FilterSet):
    company = ContractViewFieldsFilter(field_name='bidding__company__id')
    client = ContractViewFieldsFilter(field_name='bidding__client__id')
    is_outdated = django_filters.CharFilter(method='filter_is_outdated')

    class Meta:
        model = Contract
        fields = {
          'bidding': ['exact'],
          'status': ['exact'],
          'scope': ['exact'],
          'type': ['exact'],
          'number': ['exact'],
          'state': ['exact'],
          'date_start': ['lte', 'gte', 'exact'],
          'date_finish': ['lte', 'gte', 'exact'],
          'email': ['exact'],
        }

    def filter_is_outdated(self, queryset, name, value):
        contract_list = []
        value_filter = value.lower() == 'true'

        for contract in queryset:
            contract_serializer = ContractSerializer(contract)
            if(contract_serializer.data['is_outdated'] == value_filter):
                contract_list.append(contract_serializer.data['id'])

        contract_queryset = Contract.objects.filter(id__in=contract_list)
        return contract_queryset

class ContractViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ContractSerializer
    pagination_class = ContractPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'bidding__uasg',
        'bidding__client__name',
        'bidding__company__corporate_name',
        'status__name',
        'scope__name',
        'type__name',
        'date_start',
        'date_finish',
        'number',
        'observation',
        'state',
        'email',
    ]

    ordering_fields = [
        'id',
        'number',
        'date_start',
        'date_finish',
        'number',
        'observation',
        'state',
        'email',
    ]

    ordering = ['number']

    filter_class = ContractViewFilter

    def get_queryset(self):
        return Contract.objects.all().order_by('pk')

class ContractItemViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ContractItemSerializer
    pagination_class = ContractPagination
    filter_backends = [filters.SearchFilter]

    search_fields = [
        'id',
        'name',
        'observation',
    ]

    def get_queryset(self):
        return ContractItem.objects.all().order_by('pk')

class ContractItemsToCommitmentViewSet(ModelViewSetCached):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ContractItemsToCommitmentSerializer
    pagination_class = ContractPagination

    def get_queryset(self):
        queryset = Contract.objects.all().order_by('pk')
        return queryset.filter(id=self.kwargs.get('pk'))

class ContractFilterViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ContractFilterSerializer
    pagination_class = ContractPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return ContractFilter.objects.all().order_by('pk')

class ContractHistoryViewSet(ModelViewSet):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ContractHistorySerializer
    pagination_class = ContractPagination

    def get_queryset(self):
        return Contract.objects.all().order_by('pk')

class ContractListViewSet(ModelViewSetCached):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ContractListSerializer
    pagination_class = ContractPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'id',
        'bidding__uasg',
        'bidding__client__name',
        'bidding__company__corporate_name',
        'status__name',
        'scope__name',
        'type__name',
        'date_start',
        'date_finish',
        'number',
        'observation',
        'state',
        'email',
    ]

    ordering_fields = [
        'id',
        'number',
        'bidding__client__name',
        'status__name',
        'type__name',
        'date_start',
        'date_finish',
        'number',
        'state',
    ]

    ordering = ['number']

    filter_class = ContractViewFilter

    def get_queryset(self):
        return Contract.objects.select_related('bidding',
                                               'bidding__client',
                                               'bidding__company',
                                               'status',
                                               'type'
                                               ).order_by('pk')
