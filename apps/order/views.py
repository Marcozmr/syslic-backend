import logging

from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authtoken.models import Token

from django.db.models import Sum, F

from django_filters import rest_framework as django_filters
from django_filters import FilterSet
from django_filters import Filter

from apps.utils.cache import ModelViewSetCached

from .models import (
    Order,
    OrderInterest,
    OrderFile,
    OrderCommitmentStatus,
    OrderCommitment,
    OrderCommitmentItem,
    OrderCommitmentItemProduct,
    OrderCommitmentFilter,
    OrderCommitmentFile,
    OrderDeliveryStatus,
    OrderDelivery,
    OrderDeliveryFilter,
    OrderDeliveryItem,
    OrderDeliveryFile,
    OrderDeliveryFreightCotation,
    OrderFilter,
    OrderAssistance,
    OrderAssistanceStatus,
    OrderAssistanceType,
    OrderAssistanceFilter,
    OrderAuditPercentage,
    OrderInvoicingFilter,
    OrderInvoicingStatus,
    OrderInvoicingFile,
    OrderInvoicing,
)

from .serializers import (
    OrderSerializer,
    OrderListSerializer,
    OrderInterestSerializer,
    OrderFileSerializer,
    OrderCommitmentStatusSerializer,
    OrderCommitmentSerializer,
    OrderCommitmentFilterSerializer,
    OrderCommitmentItemSerializer,
    OrderCommitmentItemProductSerializer,
    OrderCommitmentFileSerializer,
    OrderCommitmentSituationSerializer,
    OrderItemsToCommitmentSerializer,
    OrderItemsReportSerializer,
    OrderDeliveryStatusSerializer,
    OrderDeliverySerializer,
    OrderDeliveryFilterSerializer,
    OrderDeliveryItemSerializer,
    OrderDeliveryFileSerializer,
    OrderItemsToDeliverySerializer,
    OrderDeliveryFreightCotationSerializer,
    OrderFilterSerializer,
    OrderHistorySerializer,
    OrderCommitmentHistorySerializer,
    OrderDeliveryHistorySerializer,
    OrderAssistanceSerializer,
    OrderAssistanceListSerializer,
    OrderAssistanceBasicSerializer,
    OrderToAssistanceSerializer,
    OrderAssistanceStatusSerializer,
    OrderAssistanceTypeSerializer,
    OrderAssistanceFilterSerializer,
    OrderProductsSerializer,
    OrderAuditPercentageSerializer,
    OrderDeliverySituationSerializer,
    OrderInvoicingFilterSerializer,
    OrderInvoicingStatusSerializer,
    OrderInvoicingFileSerializer,
    OrderInvoicingSerializer,
    OrderInvoicingViewSerializer,
    OrderInvoicingListSerializer,
    OrderInvoicingCreateSerializer,
    OrderInvoicingSituationSerializer,
    OrderCommitmentListSerializer,
    OrderDeliveryListSerializer,
)

from apps.contract.models import (
    ContractItem,
)

from .pagination import (
    OrderPagination,
)

from .permissions import (
    HasModelPermission,
    HasModelSettingsPermission,
    HasOtherPermission,
)

class OrderInterestViewSet(ModelViewSetCached):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = OrderInterestSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return OrderInterest.objects.all().order_by('pk')

class orderViewFieldsFilter(Filter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(**{self.field_name: value})
        return qs
    
class OrderViewFilter(FilterSet):
    uasg = orderViewFieldsFilter(field_name='contract__bidding__uasg')
    trade_number = orderViewFieldsFilter(field_name='contract__bidding__trade_number')
    client = orderViewFieldsFilter(field_name='contract__bidding__client__id')
    company = orderViewFieldsFilter(field_name='company__id')
    interest = orderViewFieldsFilter(field_name='interest__id')
    date_expiration = django_filters.DateFromToRangeFilter()
    date_expiration_gte = django_filters.DateFilter(field_name='date_expiration', lookup_expr='gte')
    date_expiration_lte = django_filters.DateFilter(field_name='date_expiration', lookup_expr='lte')

    class Meta:
        model = Order
        fields = {
            'owner': ['exact'],
            'date_expiration': ['lte', 'gte', 'exact'],
            'nf_payed': ['exact'],
        }

class OrderViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderSerializer
    pagination_class = OrderPagination

    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'id',
        'contract__bidding__uasg',
        'contract__bidding__trade_number',
        'contract__bidding__client__name',
        'interest__name',
        'company__corporate_name',
        'date_expiration',
    ]

    ordering_fields = [
        'id',
        'contract__bidding__uasg',
        'contract__bidding__trade_number',
        'contract__bidding__client__name',
        'interest__name',
        'company__corporate_name',
        'company__name_fantasy',
        'date_expiration',
        'price',
        'price_commitment',
    ]

    filter_class = OrderViewFilter

    def get_queryset(self):
        queryset = Order.objects.annotate(
                price = Sum(F('contract__items__price') * F('contract__items__quantity')),
                price_commitment = Sum(F('commitments__items__item__price') * F('commitments__items__quantity'))
                ).order_by('pk')

        return queryset

class OrderListViewSet(ModelViewSetCached):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderListSerializer
    pagination_class = OrderPagination

    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'id',
        'contract__bidding__uasg',
        'contract__bidding__trade_number',
        'contract__bidding__client__name',
        'interest__name',
        'company__corporate_name',
        'date_expiration',
    ]

    ordering_fields = [
        'id',
        'contract__bidding__uasg',
        'contract__bidding__trade_number',
        'contract__bidding__client__name',
        'interest__name',
        'company__corporate_name',
        'company__name_fantasy',
        'date_expiration',
        'price',
        'price_commitment',
    ]

    filter_class = OrderViewFilter

    def get_queryset(self):
        queryset = Order.objects.select_related(
                                    'contract',
                                    'interest',
                                    'company',
                                    'owner',
                                ) \
                                .prefetch_related(
                                    'commitments__items__item',
                                    'contract__items',
                                ) \
                                .annotate(
                                    price = Sum(
                                        F('contract__items__price') * F('contract__items__quantity')
                                    ),
                                    price_commitment = Sum(
                                        F('commitments__items__item__price') * F('commitments__items__quantity')
                                    )
                                ).order_by('pk')

        return queryset

class OrderFileViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderFileSerializer

    def get_queryset(self):
        return OrderFile.objects.all().order_by('pk')

class OrderCommitmentStatusViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderCommitmentStatusSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'name',
        'color',
        'initial',
    ]

    ordering_fields = [
        'id',
        'name',
        'initial',
    ]

    ordering = ['name']

    filter_fields = {
        'name': ['exact'],
        'initial': ['exact'],
    }

    def get_queryset(self):
        return OrderCommitmentStatus.objects.all().order_by('pk')

class CommitmentByClientFilter(Filter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(order__contract__bidding__client=value)
        return qs

class CommitmentByTradeNumberFilter(Filter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(order__contract__bidding__trade_number=value)
        return qs

class OrderCommitmentViewFilter(FilterSet):
    client = CommitmentByClientFilter()
    trade_number = CommitmentByTradeNumberFilter()
    date_delivery = django_filters.DateFromToRangeFilter()
    date_expiration = django_filters.DateFromToRangeFilter()

    class Meta:
        model = OrderCommitment
        fields = {
          'order': ['exact'],
          'company': ['exact'],
          'status': ['exact'],
          'number': ['exact'],
          'date_delivery': ['lte', 'gte', 'exact'],
          'date_expiration': ['lte', 'gte', 'exact'],
          'situation': ['exact'],
        }

class OrderCommitmentViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderCommitmentSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'order__contract__bidding__client__name',
        'order__contract__bidding__client__name_fantasy',
        'order__contract__bidding__client__cnpj',
        'order__contract__bidding__trade_number',
        'order__contract__bidding__uasg',
        'company__corporate_name',
        'status__name',
        'number',
        'date_delivery',
        'date_expiration',
        'situation',
    ]

    ordering_fields = [
        'id',
        'order__contract__bidding__client__name',
        'order__contract__bidding__trade_number',
        'company__corporate_name',
        'company__name_fantasy',
        'status__name',
        'number',
        'date_delivery',
        'date_expiration',
        'price',
        'situation',
    ]

    ordering = ['id']

    filter_class = OrderCommitmentViewFilter

    def get_queryset(self):
        queryset = OrderCommitment.objects.annotate(
            price = Sum(F('items__item__price') * F('items__quantity')),
        ).order_by('pk')

        return queryset

class OrderCommitmentListViewSet(ModelViewSetCached):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderCommitmentListSerializer
    pagination_class = OrderPagination
    filter_class = OrderCommitmentViewFilter
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend,
    ]
    
    search_fields = [
        'id',
        'order__contract__bidding__client__name',
        'order__contract__bidding__client__name_fantasy',
        'order__contract__bidding__client__cnpj',
        'order__contract__bidding__trade_number',
        'order__contract__bidding__uasg',
        'company__corporate_name',
        'status__name',
        'number',
        'date_delivery',
        'date_expiration',
        'situation',
    ]

    ordering_fields = [
        'id',
        'order__contract__bidding__client__name',
        'order__contract__bidding__trade_number',
        'company__corporate_name',
        'company__name_fantasy',
        'status__name',
        'number',
        'date_delivery',
        'date_expiration',
        'price',
        'situation',
    ]

    def get_queryset(self):
        queryset = OrderCommitment.objects \
                                  .select_related(
                                    'order',
                                    'company',
                                    'status',
                                    'order__contract__bidding__client',
                                  ).prefetch_related(
                                    'items__item',
                                  ).annotate(
                                    price = (
                                        Sum(F('items__item__price') * F('items__quantity'))
                                    ),
                                  ).order_by('pk')

        return queryset

class OrderCommitmentSituationViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderCommitmentSituationSerializer
    http_method_names = ['put']

    def get_queryset(self):
        return OrderCommitment.objects.all().order_by('pk')

class OrderCommitmentItemViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderCommitmentItemSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'commitment',
        'annotation',
    ]

    ordering_fields = [
        'id',
        'quantity',
        'deliverable',
    ]

    ordering = ['quantity']

    filter_fields = {
        'id': ['exact'],
        'item': ['exact'],
        'commitment': ['exact'],
        'deliverable': ['exact'],
    }

    def get_queryset(self):
        return OrderCommitmentItem.objects.all().order_by('pk')

class OrderCommitmentItemProductViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderCommitmentItemProductSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'item',
        'product__name',
        'cost',
    ]

    ordering_fields = [
        'id',
        'product__quantity',
        'cost',
        'product__name',
    ]

    ordering = ['product__quantity']

    filter_fields = {
        'id': ['exact'],
        'item': ['exact'],
        'product': ['exact'],
    }

    def get_queryset(self):
        return OrderCommitmentItemProduct.objects.all().order_by('pk')

class OrderItemsToCommitmentViewSet(ModelViewSetCached):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderItemsToCommitmentSerializer
    pagination_class = OrderPagination

    cache_related_model_classes = [
            OrderCommitmentItemProduct,
            OrderCommitmentItem
    ]

    def get_queryset(self):
        queryset = Order.objects.all().order_by('pk')
        return queryset.filter(id=self.kwargs.get('pk'))

class OrderCommitmentFilterViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderCommitmentFilterSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return OrderCommitmentFilter.objects.all().order_by('pk')

class OrderCommitmentFileViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderCommitmentFileSerializer

    def get_queryset(self):
        return OrderCommitmentFile.objects.all().order_by('pk')

class OrderItemsReportViewSet(ModelViewSet):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderItemsReportSerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        queryset = Order.objects.all().order_by('pk')
        return queryset.filter(id=self.kwargs.get('pk'))

class OrderDeliveryStatusViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderDeliveryStatusSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'name',
        'color',
        'initial',
    ]

    ordering_fields = [
        'id',
        'name',
        'initial',
    ]

    ordering = ['name']

    filter_fields = {
        'name': ['exact'],
        'initial': ['exact'],
    }

    def get_queryset(self):
        return OrderDeliveryStatus.objects.all().order_by('pk')
    
class DeliveryByClientFilter(Filter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(order__contract__bidding__client=value)
        return qs

class DeliveryByTradeNumberFilter(Filter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(order__contract__bidding__trade_number=value)
        return qs

class DeliveryByIdFilter(Filter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(id=value)
        return qs

class DeliveryByCommitmentItemFilter(Filter):
    def filter(self, qs, value):
        if value:
            item_queryset = OrderCommitmentItem.objects.filter(commitment=value)
            item_delivery_queryset = OrderDeliveryItem.objects.filter(item__in=item_queryset)
            delivery_list = list(item_delivery_queryset.values_list('delivery', flat=True))
            qs = qs.filter(id__in=delivery_list)
        return qs

class OrderDeliveryViewFilter(FilterSet):
    client = DeliveryByClientFilter()
    trade_number = DeliveryByTradeNumberFilter()
    date_delivery = django_filters.DateFromToRangeFilter()
    delivery_number = DeliveryByIdFilter()
    commitment = DeliveryByCommitmentItemFilter()

    class Meta:
        model = OrderDelivery
        fields = {
          'order': ['exact'],
          'company': ['exact'],
          'status': ['exact'],
          'date_delivery': ['lte', 'gte', 'exact'],
          'carrier': ['exact'],
          'city': ['exact'],
          'state': ['exact'],
          'country': ['exact'],
          'zip_code': ['exact'],
          'situation': ['exact'],
          'expedition_date': ['lte', 'gte', 'exact'],
          'invoicing_delivery_date': ['lte', 'gte', 'exact'],
        }

class OrderDeliveryViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderDeliverySerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'id',
        'order__contract__bidding__client__name',
        'order__contract__bidding__client__name_fantasy',
        'order__contract__bidding__trade_number',
        'order__contract__bidding__uasg',
        'company__corporate_name',
        'company__name_fantasy',
        'freight_cost',
        'carrier__name',
        'carrier__name_fantasy',
        'date_delivery',
        'status__name',
        'annotation',
        'address',
        'neighborhood',
        'complement',
        'number',
        'city__name',
        'state__name',
        'state__code',
        'country__name',
        'zip_code',
        'expedition_date',
        'invoicing_delivery_date',
        'annotation',
        'driver_name',
    ]

    ordering_fields = [
        'id',
        'order__contract__bidding__client__name',
        'order__contract__bidding__client__name_fantasy',
        'order__contract__bidding__trade_number',
        'order__contract__bidding__uasg',
        'company__corporate_name',
        'company__name_fantasy',
        'commitment__number',
        'freight_estimated',
        'freight_cost',
        'freight_real',
        'total_value',
        'carrier__name',
        'carrier__name_fantasy',
        'date_delivery',
        'status__name',
        'annotation',
        'address',
        'neighborhood',
        'complement',
        'number',
        'city__name',
        'state__name',
        'state__code',
        'country__name',
        'zip_code',
        'invoicing_delivery_date',
        'annotation',
        'driver_name',
    ]

    ordering = ['id']

    filter_class = OrderDeliveryViewFilter

    def get_queryset(self):
        queryset = OrderDelivery.objects \
                                .select_related(
                                    'order',
                                    'order__contract__bidding__client',
                                    'company',
                                    'status',
                                    'carrier',
                                    'city',
                                    'state',
                                    'country',
                                ) \
                                .prefetch_related(
                                    'items__item__item',
                                    'file',
                                    'cotations',
                                ) \
                                .annotate(
                                    freight_estimated = Sum(
                                        (F('items__item__item__price')) * \
                                        (F('items__quantity')) * \
                                        (F('items__item__item__freight')/100),
                                        distinct=True
                                    ),
                                    total_value = Sum(
                                        F('items__item__item__price') * F('items__quantity'),
                                        distinct=True
                                    ),
                                    freight_real = Sum(
                                        F('cotations__cost'), filter=F('cotations__accepted'),
                                        distinct=True
                                    ),
                                ).order_by('pk')

        return queryset

class OrderDeliveryListViewSet(ModelViewSetCached):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderDeliveryListSerializer
    pagination_class = OrderPagination
    filter_class = OrderDeliveryViewFilter
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend
    ]

    search_fields = [
        'id',
        'order__contract__bidding__client__name',
        'order__contract__bidding__client__name_fantasy',
        'order__contract__bidding__trade_number',
        'order__contract__bidding__uasg',
        'company__corporate_name',
        'company__name_fantasy',
        'freight_cost',
        'carrier__name',
        'carrier__name_fantasy',
        'date_delivery',
        'status__name',
        'annotation',
        'address',
        'neighborhood',
        'complement',
        'number',
        'city__name',
        'state__name',
        'state__code',
        'country__name',
        'zip_code',
        'expedition_date',
        'invoicing_delivery_date',
        'annotation',
        'driver_name',
    ]

    ordering_fields = [
        'id',
        'order__contract__bidding__client__name',
        'order__contract__bidding__client__name_fantasy',
        'order__contract__bidding__trade_number',
        'company__corporate_name',
        'company__name_fantasy',
        'freight_estimated',
        'freight_real',
        'total_value',
        'carrier__name',
        'carrier__name_fantasy',
        'status__name',
        'date_delivery',
        'invoicing_delivery_date',
    ]    

    def get_queryset(self):
        queryset = OrderDelivery.objects \
                                .select_related(
                                    'order',
                                    'company',
                                    'status',
                                    'carrier',
                                ) \
                                .prefetch_related(
                                    'items__item__item'
                                ) \
                                .annotate(
                                    freight_estimated = Sum(
                                        (F('items__item__item__price')) * \
                                        (F('items__quantity')) * \
                                        (F('items__item__item__freight')/100),
                                        distinct=True
                                    ),
                                    total_value = Sum(
                                        F('items__item__item__price') * F('items__quantity'),
                                        distinct=True
                                    ),
                                    freight_real = Sum(
                                        F('cotations__cost'), filter=F('cotations__accepted'),
                                        distinct=True
                                    ),
                                ).order_by('pk')

        return queryset

class OrderDeliveryFilterViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderDeliveryFilterSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return OrderDeliveryFilter.objects.all().order_by('pk')

class OrderDeliveryItemViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderDeliveryItemSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'delivery',
        'item',
        'quantity',
    ]

    ordering_fields = [
        'id',
        'quantity',
        'delivery',
        'item',
    ]

    ordering = ['delivery', 'quantity']

    filter_fields = {
        'id': ['exact'],
        'item': ['exact'],
        'delivery': ['exact'],
    }

    cache_related_model_classes = [
        OrderCommitmentItemProduct,
        OrderCommitmentItem,
        OrderDelivery,
        ContractItem,
    ]

    def get_queryset(self):
        return OrderDeliveryItem.objects \
                                 .select_related(
                                    'delivery'
                                 ) \
                                 .prefetch_related(
                                    'item__item__items',
                                    'item__products__product'
                                 ) \
                                 .order_by('pk')

class OrderDeliveryFreightCotationViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderDeliveryFreightCotationSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'delivery',
        'carrier',
        'email',
        'phone_number',
        'cost',
        'date_cotation',
        'accepted',
        'quote_number',
    ]

    ordering_fields = [
        'id',
        'delivery',
        'carrier',
        'cost',
        'date_cotation',
        'accepted',
        'quote_number',
    ]

    ordering = ['delivery', 'date_cotation', 'accepted', 'quote_number']

    filter_fields = {
        'id': ['exact'],
        'delivery': ['exact'],
        'carrier': ['exact'],
        'email': ['exact'],
        'phone_number': ['exact'],
        'cost': ['lte', 'gte', 'exact'],
        'date_cotation': ['lte', 'gte', 'exact'],
        'accepted': ['exact'],
        'quote_number': ['exact'],
    }

    def get_queryset(self):
        return OrderDeliveryFreightCotation.objects.all().order_by('pk')

class OrderDeliveryFileViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderDeliveryFileSerializer

    def get_queryset(self):
        return OrderDeliveryFile.objects.all().order_by('pk')

class OrderItemsToDeliveryViewSet(ModelViewSetCached):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderItemsToDeliverySerializer
    pagination_class = OrderPagination

    cache_related_model_classes = [
        OrderCommitmentItemProduct,
        OrderCommitmentItem,
        OrderDeliveryItem,
        OrderCommitment,
        OrderDelivery,
        ContractItem,
    ]

    def get_queryset(self):
        queryset = OrderDelivery.objects.all().order_by('pk')
        return queryset.filter(id=self.kwargs.get('pk'))

class OrderFilterViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderFilterSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return OrderFilter.objects.all().order_by('pk')

class OrderHistoryViewSet(ModelViewSet):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderHistorySerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        return Order.objects.all().order_by('pk')

class OrderCommitmentHistoryViewSet(ModelViewSet):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderCommitmentHistorySerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        return OrderCommitment.objects.all().order_by('pk')

class OrderDeliveryHistoryViewSet(ModelViewSet):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderDeliveryHistorySerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        return OrderDelivery.objects.all().order_by('pk')

class OrderAssistanceViewFilter(FilterSet):
    client = orderViewFieldsFilter(field_name='order__contract__bidding__client__id')
    date_scheduled = django_filters.DateFromToRangeFilter()
    date_scheduled_gte = django_filters.DateFilter(field_name='date_scheduled', lookup_expr='gte')
    date_scheduled_lte = django_filters.DateFilter(field_name='date_scheduled', lookup_expr='lte')

    class Meta:
        model = OrderAssistance
        fields = {
            'order': ['exact'],
            'status': ['exact'],
            'type': ['exact'],
            'date_scheduled': ['lte', 'gte', 'exact'],
        }

class OrderAssistanceFilterViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderAssistanceFilterSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return OrderAssistanceFilter.objects.all().order_by('pk')
    
class OrderAssistanceViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderAssistanceSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'id',
        'technician_name',
        'status__name',
        'type__name',
        'product__name',
        'order__contract__bidding__client__name',
        'order__contract__bidding__client__name_fantasy',
        'order__contract__bidding__client__cnpj',
        'order__contract__bidding__trade_number',
        'order__contract__bidding__uasg',
    ]

    ordering_fields = [
        'id',
        'order',
        'date_scheduled'
        'technician_name',
        'status__name',
        'type__name',
        'product__name',
        'order__contract__bidding__client__name',
        'order__contract__bidding__client__name_fantasy',
        'order__contract__bidding__client__cnpj',
        'order__contract__bidding__trade_number',
        'order__contract__bidding__uasg',
    ]
    
    filter_class = OrderAssistanceViewFilter
    
    ordering = ['id', 'order', 'date_scheduled']

    def get_queryset(self):
        return OrderAssistance.objects.all().order_by('pk')

class OrderAssistanceListViewSet(ModelViewSetCached):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderAssistanceListSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'id',
        'technician_name',
        'status__name',
        'type__name',
        'product__name',
        'order__contract__bidding__client__name',
        'order__contract__bidding__client__name_fantasy',
    ]

    ordering_fields = [
        'id',
        'order',
        'date_scheduled'
        'technician_name',
        'status__name',
        'type__name',
        'product__name',
        'order__contract__bidding__client__name',
        'order__contract__bidding__client__name_fantasy',
    ]
    
    filter_class = OrderAssistanceViewFilter
    
    ordering = ['id', 'order', 'date_scheduled']

    def get_queryset(self):
        return OrderAssistance.objects.select_related('status',
                                                      'type',
                                                      'product',
                                                      'order',)

class OrderAssistanceBasicViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderAssistanceBasicSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'id',
        'technician_name',
        'status__name',
        'type__name',
        'product__name',
        'order__contract__bidding__client__name',
        'order__contract__bidding__client__name_fantasy',
    ]

    ordering_fields = [
        'id',
        'order',
        'date_scheduled'
        'technician_name',
        'status__name',
        'type__name',
        'product__name',
        'order__contract__bidding__client__name',
        'order__contract__bidding__client__name_fantasy',
    ]
    
    filter_class = OrderAssistanceViewFilter
    
    ordering = ['id', 'order', 'date_scheduled']

    def get_queryset(self):
        return OrderAssistance.objects.select_related('status',
                                                      'type',
                                                      'product',
                                                      'order',)
class OrderToAssistanceViewSet(ModelViewSetCached):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderToAssistanceSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'contract__bidding__client__name',
        'contract__bidding__client__name_fantasy',
        'contract__bidding__client__phone_number',
    ]

    ordering_fields = [
        'id',
        'contract__bidding__client__name',
        'contract__bidding__client__name_fantasy',
        'contract__bidding__client__phone_number',
    ]

    ordering = ['contract']

    filter_fields = {
        'id': ['exact'],
        'contract': ['exact'],
    }

    def get_queryset(self):
        return Order.objects.select_related('contract',)

class OrderAssistanceStatusViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderAssistanceStatusSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'name',
        'color',
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
        return OrderAssistanceStatus.objects.all().order_by('pk')
    
class OrderAssistanceTypeViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderAssistanceTypeSerializer
    pagination_class = OrderPagination
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
        return OrderAssistanceType.objects.all().order_by('pk')

class OrderProductsViewSet(ModelViewSet):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderProductsSerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        queryset = Order.objects.all().order_by('pk')
        return queryset.filter(id=self.kwargs.get('pk'))

class OrderAuditPercentageAPIView(RetrieveUpdateAPIView):
    http_method_names = ['get', 'put', 'patch', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderAuditPercentageSerializer
    
    def get_object(self):
        auth_header = self.request.headers.get('Authorization')
        token_key = auth_header.split()[1]
        token = Token.objects.get(key=token_key)
        user = token.user

        instance, created = OrderAuditPercentage.objects.get_or_create(pk=user.profile.context_account.id)
        return instance

class OrderDeliverySituationViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderDeliverySituationSerializer
    http_method_names = ['put']

    def get_queryset(self):
        return OrderDelivery.objects.all().order_by('pk')

class OrderInvoicingStatusViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderInvoicingStatusSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'name',
        'color',
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
        return OrderInvoicingStatus.objects.all().order_by('pk')

class OrderInvoicingFileViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderInvoicingFileSerializer

    cache_related_model_classes = [
            OrderInvoicing,
    ]

    def get_queryset(self):
        return OrderInvoicingFile.objects.all().order_by('pk')

class InvoicingByOrderFilter(Filter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(commitment__order=value)
        return qs

class InvoicingByCompanyFilter(Filter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(commitment__order__company=value)
        return qs

class InvoicingByClientFilter(Filter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(commitment__order__contract__bidding__client=value)
        return qs

class InvoicingByTradeNumberFilter(Filter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(commitment__order__contract__bidding__trade_number=value)
        return qs

class InvoicingByCommitmentNumberFilter(Filter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(commitment__number=value)
        return qs

class InvoicingByCarrierFilter(Filter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(delivery__carrier=value)
        return qs

class InvoicingByIsPayedFilter(Filter):
    def filter(self, qs, value):
        if value == 'true':
            qs = qs.exclude(real_pay_date__isnull=True)

        elif value == 'false':
            qs = qs.filter(real_pay_date__isnull=True)

        return qs

class OrderInvoicingViewFilter(FilterSet):
    order = InvoicingByOrderFilter()
    company = InvoicingByCompanyFilter()
    commitment_number = InvoicingByCommitmentNumberFilter()
    carrier = InvoicingByCarrierFilter()
    nf_payed = InvoicingByIsPayedFilter()
    client = InvoicingByClientFilter()
    trade_number = InvoicingByTradeNumberFilter()
    invoicing_date = django_filters.DateFromToRangeFilter()
    expected_payment_date = django_filters.DateFromToRangeFilter()
    real_pay_date = django_filters.DateFromToRangeFilter()
    date_delivery = django_filters.DateFromToRangeFilter(
        field_name = 'delivery__date_delivery',
    )
    invoicing_delivery_date = django_filters.DateFromToRangeFilter(
        field_name = 'delivery__invoicing_delivery_date',
    )

    class Meta:
        model = OrderInvoicing
        fields = {
          'status': ['exact'],
          'delivery': ['exact'],
          'commitment': ['exact'],
          'note_number': ['exact'],
          'invoicing_date': ['lte', 'gte', 'exact'],
          'expected_payment_date': ['lte', 'gte', 'exact'],
          'real_pay_date': ['lte', 'gte', 'exact'],
          'situation': ['exact'],
        }

class OrderInvoicingFilterViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderInvoicingFilterSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return OrderInvoicingFilter.objects.all().order_by('pk')

class OrderInvoicingViewSet(ModelViewSetCached):
    http_method_names = ['get', 'put', 'delete', 'patch', 'options']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderInvoicingSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    cache_related_model_classes = [
            OrderInvoicingFile,
    ]
    
    search_fields = [
        'id',
        'delivery__id',
        'delivery__date_delivery',
        'commitment__number',
        'commitment__order__contract__bidding__client__name',
        'note_number',
        'invoicing_date',
        'expected_payment_date',
        'real_pay_date',
        'annotation',
        'status__name',
    ]
    
    ordering_fields = [
        'id',
        'delivery',
        'delivery__date_delivery',
        'commitment__number',
        'commitment__order__contract__bidding__client__name',
        'note_number',
        'invoicing_date',
        'expected_payment_date',
        'real_pay_date',
        'status__name',
    ]
    
    ordering = ['note_number', 'invoicing_date', 'expected_payment_date', 'real_pay_date']
    
    filter_class = OrderInvoicingViewFilter

    
    def get_queryset(self):
        return OrderInvoicing.objects.all().order_by('pk')

class OrderInvoicingListViewSet(ModelViewSetCached):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderInvoicingListSerializer
    pagination_class = OrderPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    
    search_fields = [
        'id',
        'delivery__id',
        'delivery__date_delivery',
        'delivery__invoicing_delivery_date',
        'commitment__number',
        'commitment__order__contract__bidding__client__name',
        'note_number',
        'invoicing_date',
        'expected_payment_date',
        'real_pay_date',
        'annotation',
        'status__name',
    ]
    
    ordering_fields = [
        'id',
        'delivery',
        'delivery__date_delivery',
        'delivery__invoicing_delivery_date',
        'commitment__number',
        'commitment__order__contract__bidding__client__name',
        'note_number',
        'invoicing_date',
        'expected_payment_date',
        'real_pay_date',
        'status__name',
        'liquid_margin',
        'total_nf',
    ]
    
    ordering = ['note_number', 'invoicing_date', 'expected_payment_date', 'real_pay_date']
    
    filter_class = OrderInvoicingViewFilter

    def get_queryset(self):
        return OrderInvoicing.objects.all().order_by('pk')

class OrderInvoicingViewViewSet(ModelViewSetCached):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderInvoicingViewSerializer

    cache_related_model_classes = [
            OrderInvoicingFile,
            OrderInvoicing,
    ]

    def get_queryset(self):
        return OrderInvoicing.objects.all().order_by('pk')

class OrderInvoicingCreateViewSet(ModelViewSetCached):
    http_method_names = ['post', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderInvoicingCreateSerializer

    def get_queryset(self):
        return OrderInvoicing.objects.all().order_by('pk')

class OrderDeliveryHasInvoicingViewSet(APIView):
    permission_classes = (HasModelPermission, HasOtherPermission) 

    def get(self, request, delivery_id):
        try:
            delivery = OrderDelivery.objects.get(id=delivery_id)
        except OrderDelivery.DoesNotExist:
            return Response({"error": "Delivery does not exist"}, status=status.HTTP_404_NOT_FOUND)

        invoicing_queryset = OrderInvoicing.objects.filter(delivery=delivery)

        has_invoicing = invoicing_queryset.exists()
        invoicing_list = []
        next_situation = 'released'
        has_invoicing_done = False

        for invoicing in invoicing_queryset:
            invoicing_serializer = OrderInvoicingSerializer(invoicing).data

            invoicing_list.append(invoicing_serializer['id'])
            
            if(invoicing_serializer['situation'] != 'done' and invoicing_serializer['situation'] != 'released'):
                next_situation = 'invoicing'

            if(invoicing_serializer['situation'] == 'done'):
                has_invoicing_done = True

        if(not has_invoicing):
           next_situation = 'idle' 

        data = {
            'delivery': delivery_id,
            'has_invoicing': has_invoicing,
            'invoicing_list': invoicing_list,
            'next_situation': next_situation,
            'has_invoicing_done': has_invoicing_done,
        }

        return Response(data, status=status.HTTP_200_OK)

class OrderInvoicingSituationViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = OrderInvoicingSituationSerializer
    http_method_names = ['put']

    def get_queryset(self):
        return OrderInvoicing.objects.all().order_by('pk')

class OrderInvoicingItemsViewSet(ModelViewSetCached):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission, HasOtherPermission) 
    pagination_class = OrderPagination
    serializer_class = OrderInvoicingSerializer

    cache_model_class = OrderInvoicing

    def get_queryset(self):
        return OrderInvoicing.objects.all().order_by('pk')

    def retrieve(self, request, pk):
        if self.cache_enable:
            try:
                data = self.cache_manager.get(self.cache_model, request, pk)
                if data is not None:
                    return Response(data)
            
            except Exception as e:
                logging.error(f"""
                    [CACHE ERROR]: (retrieve): {self.cache_model} model using cache.
                    [ERROR]: {e}"""
                )

            response = self.get_invoicing_item_list(request, pk)

            try:
                self.cache_manager.set(self.cache_model, response.data, self.cache_timeout, request, pk)
            except Exception as e:
                logging.error(f"""
                    [CACHE ERROR]: (retrieve): {self.cache_model} model using cache.
                    [ERROR]: {e}"""
                )

            return response

        else:
            return self.get_invoicing_item_list(request, pk)

    def get_invoicing_item_list(self, request, pk):
        invoicing_item_list = []
        invoicing_queryset = OrderInvoicing.objects.filter(id=pk)

        if invoicing_queryset.exists():
            invoicing_serializer = OrderInvoicingSerializer(invoicing_queryset.first()).data

            items_queryset = OrderDeliveryItem.objects.filter(delivery=invoicing_serializer['delivery'], item__commitment=invoicing_serializer['commitment'])

            page_number = request.GET.get('p', 1)
            paginator = self.pagination_class()
            page_obj = paginator.paginate_queryset(items_queryset, request)

            for item in page_obj:
                items_serializer = OrderDeliveryItemSerializer(item).data
                invoicing_item_list.append(items_serializer)

            data = {
                'total_pages': paginator.page.paginator.num_pages,
                'current_page': page_number,
                'total_items': len(items_queryset),
                'invoicing_id': pk,
                'invoicing_items': invoicing_item_list,
            }

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invoicing does not exist"}, status=status.HTTP_404_NOT_FOUND)
