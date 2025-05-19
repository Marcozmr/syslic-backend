from rest_framework import filters
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as django_filters
from django.db.models import Q

from apps.utils.cache import ModelViewSetCached

from .models import (
    Commission,
)

from .serializers import (
    CommissionSerializer,
    CommissionInvoicingSerializer,
    CommissionUserValuesSerializer,
)

from .pagination import (
    CommissionPagination,
)

from .permissions import (
    HasModelPermission,
    IsAuthenticated,
)

from apps.accounts.models import (
    User,
    Profile,
)

from apps.order.models import (
    OrderInvoicing,
)

from apps.order.views import (
    OrderInvoicingViewFilter,
)

from apps.permission.models import (
    PermissionOptions,
)

class CommissionViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | IsAuthenticated,)
    serializer_class = CommissionSerializer
    pagination_class = CommissionPagination

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend
    ]

    search_fields = [
        'id',
        'notes,'
        'owner__first_name',
        'owner__last_name',
        'invoicing__invoicing_date',
        'invoicing__expected_payment_date',
        'invoicing__real_pay_date',
        'invoicing__note_number',
    ]

    ordering_fields = [
        'id',
        'owner__first_name',
        'owner__last_name',
        'invoicing__invoicing_date',
        'invoicing__expected_payment_date',
        'invoicing__real_pay_date',
        'invoicing__note_number',
    ]

    filter_fields = {
        'id': ['exact'],
        'invoicing': ['exact'],
    }

    cache_related_model_classes = [
        User,
        Profile,
        Commission,
        OrderInvoicing,
    ]

    def get_queryset(self):
        return Commission.objects.all()

class OrderInvoicingIsDoneViewSet(ModelViewSet):
    serializer_class = CommissionInvoicingSerializer
    pagination_class = CommissionPagination
    filter_class = OrderInvoicingViewFilter
    permission_classes = (HasModelPermission | IsAuthenticated,)

    http_method_names = [
        'get',
        'options',
        'head'
    ]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend
    ]

    search_fields = [
        'id',
        'note_number',
        'status__name',
        'delivery__date_delivery',
        'delivery__invoicing_delivery_date',
        'annotation',
        'commitment__order__company__corporate_name',
        'commitment__order__contract__bidding__client__name',
        'commitment__order__contract__bidding__client__name_fantasy',
        'commitment__order__contract__bidding__client__cnpj',
        'commitment__order__contract__bidding__trade_number',
        'commitment__order__contract__bidding__uasg',
    ]

    ordering_fields = [
        'id',
        'note_number',
        'invoicing_date',
        'expected_payment_date',
        'real_pay_date',
        'annotation',
        'situation',
        'status__name',
        'delivery__date_delivery',
        'delivery__invoicing_delivery_date',
        'commitment__order',
        'commitment__order__company__corporate_name',
        'commitment__order__contract__bidding__client__name',
        'commitment__order__contract__bidding__client__name_fantasy',
        'commitment__order__contract__bidding__client__cnpj',
        'commitment__order__contract__bidding__trade_number',
        'commitment__order__contract__bidding__uasg',
        'commission_invoicing__status',
    ]

    ordering = [
        'id'
    ]

    cache_related_model_classes = [
        User,
        Profile,
        Commission,
        OrderInvoicing,
    ]

    def get_queryset(self):
        user_uuid = self.request.query_params.get('user')
        status = self.request.query_params.get('status_commission')

        user = User.objects.get(uuid=user_uuid)
        profile = Profile.objects.get(user=user)
        commissions = Commission.objects.filter(owner=profile)
        queryset = OrderInvoicing.objects.filter(situation='done')

        if user_uuid and status:

            if ('payed' == status) or ('pending' == status):
                commissions = commissions.filter(status=status)
                invoicing_ids = [commission.invoicing.id for commission in commissions]
                queryset = queryset.filter(id__in=invoicing_ids)
            else:
                commissions = commissions.filter(status__in=['payed', 'pending'])
                invoicing_ids = [commission.invoicing.id for commission in commissions]
                queryset = queryset.exclude(id__in=invoicing_ids)


        auth_header = self.request.headers.get('Authorization')
        token_key = auth_header.split()[1]
        token = Token.objects.get(key=token_key)
        user_request = token.user

        permission_queryset = PermissionOptions.objects.filter(profile=user_request.profile.permission, app_option='Commission')
        if permission_queryset.exists():
            permission_queryset = permission_queryset.filter(Q(permission_update=True) | Q(permission_write=True))
        
            if (not permission_queryset.exists()) and (str(user_request.uuid) == str(user_uuid)):
                commissions_filter_to_user = commissions.filter(status__in=['payed', 'pending'])
                invoicing_ids = commissions_filter_to_user.values_list('invoicing', flat=True)
                queryset = queryset.filter(id__in=invoicing_ids)

        return queryset
        
class CommissionUserValuesViewSet(ModelViewSetCached):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | IsAuthenticated,)
    serializer_class = CommissionUserValuesSerializer
    pagination_class = CommissionPagination
    filter_backends = [django_filters.DjangoFilterBackend]

    filter_fields = {
        'uuid': ['exact'],
    }

    cache_related_model_classes = [
        User,
        Profile,
        Commission,
        OrderInvoicing,
    ]

    def get_queryset(self):
        auth_header = self.request.headers.get('Authorization')
        token_key = auth_header.split()[1]
        token = Token.objects.get(key=token_key)
        user = token.user

        return User.objects.filter(profile__account=user.profile.context_account.id)

    def get_serializer_context(self):
        context = {}
        date_lte = self.request.GET.get('date_lte')
        date_gte = self.request.GET.get('date_gte')
        
        if date_lte:
            context['date_lte'] = date_lte
        if date_gte:
            context['date_gte'] = date_gte
            
        return context
