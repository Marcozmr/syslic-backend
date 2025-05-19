from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from django_filters import rest_framework as django_filters
from django_filters import FilterSet
from django_filters import Filter
import requests
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views import View
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import transaction
import os

from apps.utils.cache import ModelViewSetCached

from .models import (
    BiddingType,
    Modality,
    Interest,
    Platform,
    PlatformLogin,
    Phase,
    Status,
    Dispute,
    Requirement,
    Bidding,
    BiddingItem,
    BiddingFilter,
    BiddingFile,
    BiddingImported,
    BiddingCompanyFile,
    BiddingCompanyCertificate,
)

from apps.client.models import (
        Client,
)

from apps.address.models import (
        Country,
        State,
        City,
)

from .serializers import (
    TypeSerializer,
    ModalitySerializer,
    InterestSerializer,
    PlatformSerializer,
    PlatformListSerializer,
    PlatformLoginSerializer,
    PhaseSerializer,
    StatusSerializer,
    StatusBasicSerializer,
    DisputeSerializer,
    RequirementSerializer,
    BiddingListSerializer,
    BiddingListContractSerializer,
    BiddingSerializer,
    BiddingHomologatedSerializer,
    BiddingFiledSerializer,
    BiddingItemSerializer,
    BiddingItemResultSerializer,
    BiddingFilterSerializer,
    BiddingFileSerializer,
    BiddingImportedSerializer,
    BiddingImportedSimpleSerializer,
    BiddingHistorySerializer,
    BiddingCompanyCertificateSerializer,
    BiddingCompanyFileSerializer,
    BiddingItemTypeConvertSerializer,
)

from .pagination import (
    BiddingPagination,
)

from .permissions import (
    HasModelPermission,
    HasModelSettingsPermission,
    HasOtherPermission,
)

class TypeViewSet(ModelViewSetCached):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = TypeSerializer
    pagination_class = BiddingPagination
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
        return BiddingType.objects.all().order_by('pk')

class ModalityViewSet(ModelViewSetCached):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = ModalitySerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return Modality.objects.all().order_by('pk')

class InterestViewSet(ModelViewSetCached):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = InterestSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return Interest.objects.all().order_by('pk')

class PlatformLoginViewSet(ModelViewSetCached):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = PlatformLoginSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'company__corporate_name',
        'login',
        'password',
        'observation',
        'received_email',
    ]

    def get_queryset(self):
        return PlatformLogin.objects.all().order_by('pk')

class PlatformViewSet(ModelViewSetCached):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = PlatformSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
        'link',
    ]

    def get_queryset(self):
        return Platform.objects.all().order_by('pk')

class PlatformListViewSet(ModelViewSetCached):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = PlatformListSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
        'link',
    ]

    def get_queryset(self):
        return Platform.objects.all().order_by('pk')

class DisputeViewSet(ModelViewSetCached):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = DisputeSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return Dispute.objects.all().order_by('pk')

class RequirementViewSet(ModelViewSetCached):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = RequirementSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return Requirement.objects.all().order_by('pk')

class PhaseViewSet(ModelViewSetCached):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = PhaseSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return Phase.objects.all().order_by('pk')

class StatusViewSet(ModelViewSetCached):
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = StatusSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'name',
        'phase__name',
    ]

    filter_fields = {
        'phase': ['exact'],
    }

    def get_queryset(self):
        return Status.objects.all().order_by('pk')

class StatusBasicViewSet(ModelViewSetCached):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelSettingsPermission | HasOtherPermission,)
    serializer_class = StatusBasicSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'name',
    ]

    filter_fields = {
        'phase': ['exact'],
    }

    def get_queryset(self):
        return Status.objects.all().order_by('pk')

class PhaseFilter(Filter):
    def filter(self, qs, value):
        if value:
            qs = qs.filter(status__phase=value)
        return qs

class BiddingViewFilter(FilterSet):
    phase = PhaseFilter(field_name='status__phase')
    date = django_filters.DateFromToRangeFilter()
    date_capture = django_filters.DateFromToRangeFilter()
    date_proposal = django_filters.DateFromToRangeFilter()
    date_impugnment = django_filters.DateFromToRangeFilter()
    date_clarification = django_filters.DateFromToRangeFilter()
    payment_term = django_filters.DateFromToRangeFilter()
    warranty_term = django_filters.DateFromToRangeFilter()
    deadline = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Bidding
        fields = {
          'status': ['exact'],
          'client': ['exact'],
          'platform': ['exact'],
          'freight_group': ['exact'],
          'dispute': ['exact'],
          'owner': ['exact'],
          'modality': ['exact'],
          'type': ['exact'],
          'interest': ['exact'],
          'date': ['lte', 'gte', 'exact'],
          'date_capture': ['lte', 'gte', 'exact'],
          'date_proposal': ['lte', 'gte', 'exact'],
          'date_impugnment': ['lte', 'gte', 'exact'],
          'date_clarification': ['lte', 'gte', 'exact'],
          'payment_term': ['lte', 'gte', 'exact'],
          'warranty_term': ['lte', 'gte', 'exact'],
          'deadline': ['lte', 'gte', 'exact'],
          'is_homologated': ['exact'],
          'imported': ['exact'],
          'is_filed': ['exact'],
        }

class BiddingListViewSet(ModelViewSetCached):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingListSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'client__name',
        'company__corporate_name',
        'type__name',
        'modality__name',
        'interest__name',
        'platform__name',
        'status__name',
        'phase__name',
        'owner__first_name',
        'trade_number',
        'uasg',
        'date',
        'bidding_hour',
        'date_proposal',
        'hour_proposal',
        'is_homologated',
        'imported',
        'is_filed',
    ]

    ordering_fields = [
        'id',
        'client__name',
        'company__corporate_name',
        'type__name',
        'modality__name',
        'interest__name',
        'platform__name',
        'status__name',
        'status__phase__name',
        'owner__first_name',
        'trade_number',
        'uasg',
        'date',
        'bidding_hour',
        'date_proposal',
        'hour_proposal',
        'is_homologated',
        'imported',
        'is_filed',
    ]

    ordering = ['date']

    filter_class = BiddingViewFilter

    def get_queryset(self):
        return Bidding.objects.select_related('client',
                                              'company',
                                              'type',
                                              'modality',
                                              'interest',
                                              'platform',
                                              'status',
                                              'phase',
                                              'owner',)

class BiddingListContractViewSet(ModelViewSetCached):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingListContractSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'client__name',
        'trade_number',
        'uasg',
        'is_homologated',
        'imported',
    ]

    ordering_fields = [
        'id',
        'client__name',
        'trade_number',
        'uasg',
        'is_homologated',
        'imported',
    ]

    ordering = ['date']

    filter_class = BiddingViewFilter

    def get_queryset(self):
        return Bidding.objects.select_related('client',)

class BiddingViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'id',
        'client__name',
        'company__corporate_name',
        'owner__first_name',
        'type__name',
        'modality__name',
        'interest__name',
        'platform__name',
        'freight_group__name',
        'dispute__name',
        'status__name',
        'phase__name',
        'trade_number',
        'uasg',
        'link_trade',
        'link_support',
        'date',
        'date_capture',
        'date_proposal',
        'hour_proposal',
        'date_impugnment',
        'date_clarification',
        'payment_term',
        'warranty_term',
        'deadline',
        'bidding_hour',
        'city__name',
        'state__name',
        'country__name',
        'proposal_validity',
        'additional_address',
        'additional_neighborhood',
        'additional_number',
        'additional_complement',
        'additional_city__name',
        'additional_state__name',
        'additional_country__name',
        'additional_zip_code',
        'crier',
        'phone_number',
        'email',
        'exclusive_me_epp',
        'price_registry',
        'observation',
        'is_homologated',
        'object_bidding',
        'is_filed',
    ]

    ordering_fields = [
        'id',
        'client__name',
        'company__corporate_name',
        'owner__first_name',
        'type__name',
        'modality__name',
        'interest__name',
        'platform__name',
        'freight_group__name',
        'dispute__name',
        'status__name',
        'status__phase__name',
        'trade_number',
        'uasg',
        'link_trade',
        'link_support',
        'date',
        'date_capture',
        'date_proposal',
        'hour_proposal',
        'date_impugnment',
        'date_clarification',
        'payment_term',
        'warranty_term',
        'deadline',
        'proposal_validity',
        'additional_address',
        'additional_neighborhood',
        'additional_number',
        'additional_complement',
        'additional_city__name',
        'additional_state__name',
        'additional_country__name',
        'additional_zip_code',
        'crier',
        'phone_number',
        'email',
        'exclusive_me_epp',
        'price_registry',
        'observation',
        'is_homologated',
        'object_bidding',
    ]

    ordering = ['date']

    filter_class = BiddingViewFilter

    def get_queryset(self):
        return Bidding.objects.select_related('client',
                                              'company',
                                              'owner',
                                              'type',
                                              'interest',
                                              'platform',
                                              'freight_group',
                                              'dispute',
                                              'status',
                                              'phase',
                                              'city',
                                              'state',
                                              'country',
                                              )

class BiddingHomologatedViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingHomologatedSerializer
    http_method_names = ['put']

    def get_queryset(self):
        return Bidding.objects.all().order_by('pk')
    
class BiddingFiledViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingFiledSerializer
    http_method_names = ['put']

    def get_queryset(self):
        return Bidding.objects.all().order_by('pk')

class BiddingItemViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingItemSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
        'number',
    ]

    def get_queryset(self):
        return BiddingItem.objects.all().order_by('pk')

class BiddingItemResultViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingItemResultSerializer
    http_method_names = ['put']

    def get_queryset(self):
        return BiddingItem.objects.all().order_by('pk')

class BiddingFilterViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingFilterSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        return BiddingFilter.objects.all().order_by('pk')

class BiddingFileViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingFileSerializer

    def get_queryset(self):
        return BiddingFile.objects.all().order_by('pk')

class BiddingImportedListView(ModelViewSetCached):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingImportedSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'cnpj',
        'year',
        'seq',
        'bidding',
    ]

    filter_fields = {
        'cnpj': ['exact'],
        'year': ['exact'],
        'seq': ['exact'],
        'bidding': ['exact'],
    }

    def get_queryset(self):
        return BiddingImported.objects.all().order_by('pk')

class BiddingImportedSimpleListView(ModelViewSetCached):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingImportedSimpleSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'cnpj',
        'year',
        'seq',
    ]

    filter_fields = {
        'cnpj': ['exact'],
        'year': ['exact'],
        'seq': ['exact'],
    }

    def get_queryset(self):
        return BiddingImported.objects.all().order_by('pk')

class BiddingImportedViewSet(ModelViewSetCached):
    http_method_names = ['post', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingImportedSerializer


    def get_queryset(self):
        return BiddingImported.objects.all().order_by('pk')

    @action(detail=True, methods=['post'])
    def import_bidding(self, request, pk=None):
        try:
            request_data = {
                'cnpj': request.data['cnpj'],
                'year': request.data['year'],
                'seq': request.data['seq'],
            }

            with transaction.atomic():
                bidding_response = self.perform_import_bidding(request_data)
                request_data['bidding'] = bidding_response['serialized_bidding']

                item_response = self.perform_import_items(bidding_response['bidding'], request_data)
                request_data['item'] = item_response

                attach_response = self.perform_import_attach(bidding_response['bidding'], request_data)
                request_data['attach'] = attach_response

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse(request_data, status=status.HTTP_201_CREATED)

    def perform_import_bidding(self, response_data):
        try:
            api_url = "https://pncp.gov.br/api/consulta/v1/orgaos/{cnpj}/compras/{year}/{seq}".format(cnpj=response_data['cnpj'], year=response_data['year'], seq=response_data['seq'])
            response_pncp = requests.get(api_url)
            if response_pncp.status_code == 200:
                data = response_pncp.json()

                # Get Client
                try:
                    client_query = Client.objects.filter(cnpj=data['orgaoEntidade']['cnpj'])
                    if client_query.exists():
                        client = client_query.first()

                    else:
                        country = Country.objects.get(id=1)
                        state = State.objects.get(code=data['unidadeOrgao']['ufSigla'])
                        city = City.objects.get(name__iexact=data['unidadeOrgao']['municipioNome'], state=state)
                        client = Client.objects.create(cnpj=data['orgaoEntidade']['cnpj'],
                                                       name=data['orgaoEntidade']['razaoSocial'],
                                                       name_fantasy=data['orgaoEntidade']['razaoSocial'],
                                                       country=country,
                                                       state=state,
                                                       city=city)
                except Exception as e:
                    result_error = {
                        'error': e,
                        'msg': 'fail to get client'
                    }
                    raise ValidationError(result_error)

                # Get Platform
                try:
                    platform_query = Platform.objects.filter(name=data['usuarioNome'])
                    if platform_query.exists():
                        platform = platform_query.first()
                    else:
                        platform = Platform.objects.create(name=data['usuarioNome'])
                except Exception as e:
                    result_error = {
                        'error': e,
                        'msg': 'fail to get platform'
                    }
                    raise ValidationError(result_error)

                # Get Type
                try:
                    type_query = BiddingType.objects.filter(name=data['tipoInstrumentoConvocatorioNome'])
                    if type_query.exists():
                        bidding_type = type_query.first()
                    else:
                        bidding_type = BiddingType.objects.create(name=data['tipoInstrumentoConvocatorioNome'])
                except Exception as e:
                    result_error = {
                        'error': e,
                        'msg': 'fail to get type'
                    }
                    raise ValidationError(result_error)

                # Get Modality
                try:
                    modality_query = Modality.objects.filter(name=data['modalidadeNome'])
                    if modality_query.exists():
                        modality = modality_query.first()
                    else:
                        modality = Modality.objects.create(name=data['modalidadeNome'])
                except Exception as e:
                    result_error = {
                        'error': e,
                        'msg': 'fail to get modality'
                    }
                    raise ValidationError(result_error)

                # Get Dispute
                try:
                    dispute_query = Dispute.objects.filter(name=data['modoDisputaNome'])
                    if dispute_query.exists():
                        dispute = dispute_query.first()
                    else:
                        dispute = Dispute.objects.create(name=data['modoDisputaNome'])
                except Exception as e:
                    result_error = {
                        'error': e,
                        'msg': 'fail to get dispute'
                    }
                    raise ValidationError(result_error)

                # Get Status initial
                try:
                    bidding_status = Status.objects.filter(initial=True)
                    bidding_phase = ''
                    if bidding_status.exists():
                        bidding_status = bidding_status.first()
                    else:
                        raise ValidationError('error there is no initial status for the bidding')
                except Exception as e:
                    result_error = {
                        'error': e,
                        'msg': 'fail to get bidding status initial'
                    }
                    raise ValidationError(result_error)

                # Get Phase
                try:
                    if bidding_status:
                        bidding_phase = bidding_status.phase
                    else:
                        raise ValidationError('error there is no initial status to search for the phase')
                except Exception as e:
                    result_error = {
                        'error': e,
                        'msg': 'fail to get bidding phase'
                    }
                    raise ValidationError(result_error)

                # Get Interest initial
                try:
                    interest = Interest.objects.filter(initial=True)
                    if interest.exists():
                        interest = interest.first()
                    else:
                        raise ValidationError('erro there is no initial interest for the bidding')
                except Exception as e:
                    result_error = {
                        'error': e,
                        'msg': 'fail to get interest initial'
                    }
                    raise ValidationError(result_error)

                # Create Bidding
                try:
                    date_hour_str = data['dataEncerramentoProposta']
                    date_hour = datetime.strptime(date_hour_str, "%Y-%m-%dT%H:%M:%S")

                    date = date_hour.date()
                    hour = date_hour.time()

                    country = Country.objects.get(id=1)
                    state = State.objects.get(code=data['unidadeOrgao']['ufSigla'])
                    city = City.objects.get(name__iexact=data['unidadeOrgao']['municipioNome'], state=state)

                    trade_number = f"{data['numeroCompra']}/{data['anoCompra']}"
                    
                    link_pncp = "https://pncp.gov.br/app/editais/{cnpj}/{year}/{seq}".format(
                                                                                    cnpj=response_data['cnpj'],
                                                                                    year=response_data['year'],
                                                                                    seq=response_data['seq']
                                                                                    )

                    bidding = Bidding.objects.create(client=client,
                                                     platform=platform,
                                                     date_proposal=date,
                                                     hour_proposal=hour,
                                                     trade_number=trade_number,
                                                     uasg=data['unidadeOrgao']['codigoUnidade'],
                                                     type=bidding_type,
                                                     modality=modality,
                                                     dispute=dispute,
                                                     link_support='' if data['linkSistemaOrigem'] == None else data['linkSistemaOrigem'],
                                                     link_pncp=link_pncp,
                                                     object_bidding=data['objetoCompra'],
                                                     status=bidding_status,
                                                     phase=bidding_phase,
                                                     interest=interest,
                                                     country=country,
                                                     state=state,
                                                     city=city,
                                                     imported=True,)

                    serializer = BiddingSerializer(bidding)  
                    serialized_bidding = serializer.data

                    response_bidding = {
                        'serialized_bidding': serialized_bidding,
                        'bidding': bidding,
                    }

                    BiddingImported.objects.create(cnpj=response_data['cnpj'],
                                                   year=response_data['year'],
                                                   seq=response_data['seq'],
                                                   bidding=bidding)

                    return response_bidding

                except Exception as e:
                    result_error = {
                        'error': e,
                        'msg': 'fail to create bidding'
                    }
                    raise ValidationError(result_error)
            else:

                raise ValidationError('error in pncp bidding request.')

        except Exception as e:
            raise ValueError(f'error: {e}')

    def perform_import_items(self, new_bidding, response):
        try:
            url_quantity_items = "https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras/{year}/{seq}/itens/quantidade".format(cnpj=response['cnpj'], year=response['year'], seq=response['seq'])
            response_quantity_items = requests.get(url_quantity_items)
            quantity_items = response_quantity_items.json()
            
            api_url = "https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras/{year}/{seq}/itens?tamanhoPagina={quantity}".format(cnpj=response['cnpj'], year=response['year'], seq=response['seq'], quantity=quantity_items)

            response_pncp_items = requests.get(api_url)


            if response_pncp_items.status_code == 200:
                data_list = response_pncp_items.json()

                items = []
                for data in data_list:

                    if len(data['descricao']) > 30:
                        description_truncate =  data['descricao'][:30] + "..."
                    else:
                        description_truncate = data['descricao']

                    item = BiddingItem.objects.create(type='unit',
                                                      bidding=new_bidding,
                                                      number=data['numeroItem'],
                                                      name=description_truncate,
                                                      description=data['descricao'],
                                                      quantity=data['quantidade'],
                                                      price=data['valorUnitarioEstimado'],
                                                      cost=0,
                                                      fixed_cost=0,
                                                      freight=0,
                                                      margin_min=0,
                                                      price_min=0,
                                                      tax=0)


                    serializer = BiddingItemSerializer(item)  
                    serialized_item = serializer.data
                    items.append(serialized_item)
                    
                return items

            else:
                raise ValidationError('error in pncp items request.')

        except ValueError as e:
            raise ValueError(f'error: {e}')

    def perform_import_attach(self, new_bidding, response):
        try:
            api_url = "https://pncp.gov.br/api/pncp/v1/orgaos/{cnpj}/compras/{year}/{seq}/arquivos".format(
                cnpj=response['cnpj'], year=response['year'], seq=response['seq']
            )

            response_pncp_attach = requests.get(api_url)

            if response_pncp_attach.status_code == 200:
                data_list = response_pncp_attach.json()

                attachments = []
                for data in data_list:
                    file_response = requests.get(data['uri'])

                    if file_response.status_code == 200:
                        content_disposition = file_response.headers.get('Content-Disposition')
                        file_name = ''
                        if content_disposition:
                            file_name = content_disposition.split("filename=")[-1].strip('\"')
                            _, extension = os.path.splitext(file_name)
                        
                        file_name_create = ''
                        if file_name and os.path.splitext(data['titulo'])[1] == extension:
                            file_name_create = data['titulo']
                        else:
                            file_name_create = f"{data['titulo']}{extension}"
                        
                        bidding_file = BiddingFile.objects.create(bidding=new_bidding,
                                                                  name=file_name_create)
                                                                  
                        bidding_file.file.save(file_name_create, ContentFile(file_response.content))
                        bidding_file.save()

                        serializers = BiddingFileSerializer(bidding_file)  
                        serialized_attach = serializers.data
                        attachments.append(serialized_attach)
                    else:
                        raise ValidationError(f'error file download: {file_name_create}')

                return attachments
            else:
                raise ValidationError('error in pncp attachments request.')

        except ValueError as e:
            raise ValueError(f'error: {e}')

class BiddingHistoryViewSet(ModelViewSetCached):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingHistorySerializer
    pagination_class = BiddingPagination

    def get_queryset(self):
         return Bidding.objects.all().order_by('pk')

class BiddingCompanyCertificateViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingCompanyCertificateSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'bidding__trade_number',
        'bidding__uasg',
        'document__file_name',
    ]

    ordering_fields = [
        'bidding__trade_number',
        'bidding__uasg',
        'document__file_name',
    ]

    filter_fields = {
        'bidding': ['exact'],
    }

    def get_queryset(self):
        return BiddingCompanyCertificate.objects.all().order_by('pk')

class BiddingCompanyFileViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingCompanyFileSerializer
    pagination_class = BiddingPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'bidding__trade_number',
        'bidding__uasg',
        'document__client__name',
    ]

    ordering_fields = [
        'bidding__trade_number',
        'bidding__uasg',
        'document__client__name',
    ]

    filter_fields = {
        'bidding': ['exact'],
    }

    def get_queryset(self):
        return BiddingCompanyFile.objects.all().order_by('pk')

class BiddingItemTypeConvertViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = BiddingItemTypeConvertSerializer
    http_method_names = ['put']

    def get_queryset(self):
        return BiddingItem.objects.all().order_by('pk')

