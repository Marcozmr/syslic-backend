from rest_framework import serializers
from apps.utils.fields import FileBase64Field
from apps.utils.history import HistoryRecordField

from django_multitenant.utils import get_current_tenant

from .models import (
    BiddingType,
    Modality,
    Interest,
    Platform,
    PlatformLogin,
    Phase,
    Status,
    Bidding,
    BiddingCompanyFile,
    BiddingCompanyCertificate,
    BiddingItemCompound,
    BiddingItem,
    BiddingFilter,
    BiddingFile,
    Dispute,
    Requirement,
    BiddingImported,
)

from apps.transport.serializers import (
    FreightSerializer,
)

from apps.client.serializers import (
        ClientSerializer,
        ClientNameSerializer,
        ClientBasicSerializer,
        ClientNamePhoneSerializer,
)

from apps.company.serializers import (
        CompanySerializer,
        CompanyNameSerializer,
        CompanyBasicSerializer,
        CompanyFileSerializer,
        CompanyCertificateSerializer,
)

from apps.accounts.serializers import (
    ProfileSerializer,
    ProfileBasicSerializer,
)

from apps.product.models import (
        Product,
)

from apps.product.serializers import (
        ProductSerializer,
        ProductBasicSerializer,
)

from apps.address.serializers import (
    CountrySerializer,
    StateSerializer,
    CitySerializer,
)

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiddingType
        fields = [
            'id',
            'name',
        ]

class ModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Modality
        fields = [
            'id',
            'name',
        ]

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = [
            'id',
            'name',
            'color',
            'initial',
        ]


class PlatformLoginSerializer(serializers.ModelSerializer):
    company_set = CompanyNameSerializer(source='company',
                                        read_only=True)
    class Meta:
        model = PlatformLogin
        fields = [
            'id',
            'login',
            'password',
            'observation',
            'company',
            'company_set',
            'received_email',
            'platform',
        ]

class PlatformSerializer(serializers.ModelSerializer):
    logins_set = PlatformLoginSerializer(source='logins',
                                         many=True,
                                         read_only=True)
    class Meta:
        model = Platform
        fields = [
            'id',
            'name',
            'link',
            'logins',
            'logins_set',
        ]

class PlatformListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = [
            'id',
            'name',
            'link',
        ]

class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = [
            'id',
            'name',
            'color',
        ]

class StatusSerializer(serializers.ModelSerializer):
    phase_set = PhaseSerializer(source='phase',
                                read_only=True)
    class Meta:
        model = Status
        fields = [
            'id',
            'name',
            'color',
            'phase',
            'phase_set',
            'initial',
        ]

class StatusBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
            'id',
            'name',
            'color',
            'phase',
            'initial',
        ]

class DisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = [
            'id',
            'name',
        ]

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = [
            'id',
            'name',
        ]

class BiddingItemCompoundSerializer(serializers.ModelSerializer):
    product_set = ProductBasicSerializer(source='product',
                                         read_only=True)

    class Meta:
        model = BiddingItemCompound
        fields = [
            'id',
            'item',
            'product',
            'product_set',
            'price',
            'quantity',
        ]

class BiddingItemLoteSerializer(serializers.ModelSerializer):
    product_list = BiddingItemCompoundSerializer(read_only=True,
                                                 many=True)
    class Meta:
        model = BiddingItem
        fields = [
            'id',
            'type',
            'product_list',
            'number',
            'name',
            'quantity',
            'description',
            'cost',
            'price',
            'price_min',
            'freight',
            'tax',
            'fixed_cost',
            'margin_min',
            'bidding',
            'parent',
        ]

class BiddingItemParentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiddingItem
        fields = [
            'id',
            'type',
            'name',
        ]

class BiddingItemSerializer(serializers.ModelSerializer):
    product_list = BiddingItemCompoundSerializer(read_only=True,
                                                 many=True)
    
    items_set = BiddingItemLoteSerializer(source='items',
                                          read_only=True,
                                          many=True)

    parent_set = BiddingItemParentDetailSerializer(source='parent',
                                                   read_only=True)
    class Meta:
        model = BiddingItem
        fields = [
            'id',
            'type',
            'product_list',
            'number',
            'name',
            'quantity',
            'description',
            'cost',
            'price',
            'price_min',
            'freight',
            'fob_freight',
            'tax',
            'fixed_cost',
            'margin_min',
            'bidding',
            'parent',
            'parent_set',
            'items_set',
            'observation',
            'result',
        ]

    def create(self, validated_data):
        account = get_current_tenant()
        product_list = self.context['request'].data['product_list']

        try:
            item_model = BiddingItem(**validated_data, account=account)
            item_model.full_clean()
            item_model.save()

        except Exception as e:
            raise serializers.ValidationError("Fail to create bidding item: Error: {exception}".format(exception=str(e)))

        try:
            for product in product_list:
                productModel = Product.objects.get(id=product['product'])
                BiddingItemCompound.objects.create(item=item_model,
                                            product=productModel,
                                            quantity=product['quantity'],
                                            price=product['price'],
                                            account=account)
        except Exception as e:
            item_model.delete()
            raise serializers.ValidationError("Fail to create bidding item x: Error: {exception}".format(exception=str(e)))

        return item_model

    def update(self, instance, validated_data):
        product_list = self.context['request'].data['product_list']

        try:
            # Delete itens removed from bidding item
            itemList = []
            for item in product_list:
                if ('id' in item):
                    itemList.append(item['id'])

            itemCompoundList = BiddingItemCompound.objects.filter(item=instance.id)

            for item in itemCompoundList:
                if item.id not in itemList:
                    item.delete()

            # Update and add items
            for item in product_list:
                if ('id' in item):
                    item_model = BiddingItemCompound.objects.filter(id=item['id']).update(product=item['product'],
                                                                                          quantity=item['quantity'],
                                                                                          price=item['price'],
                                                                                          item=item['item'])
                else:
                    
                    biddingItemModel = BiddingItem.objects.get(id=instance.id)
                    productModel = Product.objects.get(id=item['product'])
                    account = get_current_tenant()
                    BiddingItemCompound.objects.create(item=biddingItemModel,
                                                       product=productModel,
                                                       quantity=item['quantity'],
                                                       price=item['price'],
                                                       account=account)

            # Update item
            updateItems = BiddingItem.objects.filter(id=instance.id)
            for item in updateItems:
                for field, value in validated_data.items():
                    setattr(item, field, value)
                item.full_clean()
                item.save()
            
        except Exception as e:
            raise serializers.ValidationError("Fail to update bidding item: Error: {exception}".format(exception=str(e)))

        response = BiddingItem.objects.get(id=instance.id)
        return response

class BiddingItemResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiddingItem
        fields = [
            'id',
            'observation',
            'result',
        ]

class BiddingFileSerializer(serializers.ModelSerializer):
    file = FileBase64Field(
        required=True,
        represent_in_base64=True,
        allow_null=True,
        allow_empty_file=True
    )

    class Meta:
        model = BiddingFile
        fields = [
            'id',
            'file',
            'name',
            'bidding',
            'source'
        ]

class BiddingFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiddingFile
        fields = [
            'id',
            'name',
            'source'
        ]

class BiddingCompanyFileSerializer(serializers.ModelSerializer):
    document_set = CompanyFileSerializer(source='document',
                                         read_only=True)
    class Meta:
        model = BiddingCompanyFile
        fields = ['id',
                  'document',
                  'document_set',
                  'bidding']

class BiddingCompanyCertificateSerializer(serializers.ModelSerializer):
    document_set = CompanyCertificateSerializer(source='document',
                                                read_only=True)
    class Meta:
        model = BiddingCompanyCertificate
        fields = ['id',
                  'document',
                  'document_set',
                  'bidding']

class BiddingListContractSerializer(serializers.ModelSerializer):
    client_set = ClientNameSerializer(source='client',
                                      read_only=True)

    class Meta:
        model = Bidding
        fields = [
            'id',
            'client',
            'client_set',
            'trade_number',
            'uasg',
            'is_homologated',
        ]

class BiddingListSerializer(serializers.ModelSerializer):
    client_set = ClientNameSerializer(source='client',
                                      read_only=True)

    company_set = CompanyNameSerializer(source='company',
                                        read_only=True)

    type_set = TypeSerializer(source='type',
                              read_only=True)

    modality_set = ModalitySerializer(source='modality',
                                      read_only=True)

    interest_set = InterestSerializer(source='interest',
                                      read_only=True)

    platform_set = PlatformListSerializer(source='platform',
                                          read_only=True)

    status_set = StatusBasicSerializer(source='status',
                                       read_only=True)

    phase_set = PhaseSerializer(source='phase',
                                read_only=True)

    owner_set = ProfileBasicSerializer(source='owner',
                                       read_only=True)

    class Meta:
        model = Bidding
        fields = [
            'id',
            'client',
            'client_set',
            'company',
            'company_set',
            'type',
            'type_set',
            'modality',
            'modality_set',
            'interest',
            'interest_set',
            'platform',
            'platform_set',
            'status',
            'status_set',
            'phase',
            'phase_set',
            'owner',
            'owner_set', 
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

class BiddingSerializer(serializers.ModelSerializer):
    client_set = ClientBasicSerializer(source='client',
                                       read_only=True)

    company_set = CompanyBasicSerializer(source='company',
                                         read_only=True)

    type_set = TypeSerializer(source='type',
                              read_only=True)

    modality_set = ModalitySerializer(source='modality',
                                      read_only=True)

    interest_set = InterestSerializer(source='interest',
                                      read_only=True)

    platform_set = PlatformListSerializer(source='platform',
                                          read_only=True)

    status_set = StatusBasicSerializer(source='status',
                                  read_only=True)

    phase_set = PhaseSerializer(source='phase',
                                read_only=True)

    owner_set = ProfileBasicSerializer(source='owner',
                                       read_only=True)


    items_set = serializers.SerializerMethodField()

    file_set = BiddingFileDetailSerializer(source='file',
                                           read_only=True,
                                           many=True)

    freight_group_set = FreightSerializer(source='freight_group',
                                          read_only=True)

    country_set = CountrySerializer(source='country',
                                    read_only=True)

    state_set = StateSerializer(source='state',
                                read_only=True)

    city_set = CitySerializer(source='city',
                              read_only=True)

    dispute_set = DisputeSerializer(source='dispute',
                                    read_only=True)

    additional_country_set = CountrySerializer(source='additional_country',
                                               read_only=True)

    additional_state_set = StateSerializer(source='additional_state',
                                           read_only=True)

    additional_city_set = CitySerializer(source='additional_city',
                                         read_only=True)

    def get_items_set(self, obj):
        bidding_id = obj.id

        items_qs = BiddingItem.objects.filter(bidding=bidding_id).order_by('number')

        items_result = BiddingItemSerializer(items_qs, many=True)

        return items_result.data

    class Meta:
        model = Bidding
        fields = [
            'id',
            'client',
            'client_set',
            'company',
            'company_set',
            'type',
            'type_set',
            'modality',
            'modality_set',
            'interest',
            'interest_set',
            'platform',
            'platform_set',
            'status',
            'status_set',
            'phase',
            'phase_set',
            'owner',
            'owner_set', 
            'trade_number',
            'uasg',
            'link_trade',
            'link_support',
            'link_pncp',
            'date',
            'bidding_hour',
            'freight_group',
            'freight_group_set',
            'dispute',
            'dispute_set',
            'items_set',
            'file_set',
            'city',
            'city_set',
            'state',
            'state_set',
            'country',
            'country_set',
            'date_capture',
            'date_proposal',
            'hour_proposal',
            'date_impugnment',
            'date_clarification',
            'price_record_expiration_date',
            'payment_term',
            'warranty_term',
            'deadline',
            'proposal_validity',
            'additional_address',
            'additional_neighborhood',
            'additional_number',
            'additional_complement',
            'additional_city',
            'additional_city_set',
            'additional_state',
            'additional_state_set',
            'additional_country',
            'additional_country_set',
            'additional_zip_code',
            'crier',
            'phone_number',
            'email',
            'exclusive_me_epp',
            'price_registry',
            'observation',
            'requirements',
            'is_homologated',
            'object_bidding',
            'imported',
            'contract',
            'is_filed',
        ]
        read_only_fields = ('contract', 'items_set', 'is_filed')

class BiddingFilterSerializer(serializers.ModelSerializer):
    client_set = ClientBasicSerializer(source='client',
                                       read_only=True)

    company_set = CompanyBasicSerializer(source='company',
                                         read_only=True)

    type_set = TypeSerializer(source='type',
                              read_only=True)

    modality_set = ModalitySerializer(source='modality',
                                      read_only=True)

    interest_set = InterestSerializer(source='interest',
                                      read_only=True)

    platform_set = PlatformListSerializer(source='platform',
                                          read_only=True)

    freight_group_set = FreightSerializer(source='freight_group',
                                          read_only=True)


    dispute_set = DisputeSerializer(source='dispute',
                                    read_only=True)

    phase_set = PhaseSerializer(source='phase',
                                read_only=True)

    status_set = StatusBasicSerializer(source='status',
                                       read_only=True)

    owner_set = ProfileBasicSerializer(source='owner',
                                       read_only=True)

    class Meta:
        model = BiddingFilter
        fields = [
            'id',
            'name',
            'client',
            'client_set',
            'company',
            'company_set',
            'type',
            'type_set',
            'modality',
            'modality_set',
            'interest',
            'interest_set',
            'platform',
            'platform_set',
            'freight_group',
            'freight_group_set',
            'dispute',
            'dispute_set',
            'status',
            'phase',
            'phase_set',
            'status_set',
            'owner',
            'owner_set', 
            'date_start',
            'date_finish',
            'date_capture',
            'date_proposal',
            'hour_proposal',
            'date_impugnment',
            'date_clarification',
            'payment_term',
            'warranty_term',
            'deadline',
            'is_homologated',
            'imported',
            'is_filed',
        ]

class BiddingHomologatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bidding
        fields = [
            'id',
            'is_homologated',
        ]

class BiddingFiledSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bidding
        fields = [
            'id',
            'is_filed',
        ]

class BiddingImportedSerializer(serializers.ModelSerializer):
    bidding_set = BiddingListSerializer(source='bidding',
                                        read_only=True)
    class Meta:
        model = BiddingImported
        fields = [
            'cnpj',
            'year',
            'seq',
            'bidding',
            'bidding_set',
        ]
    
    read_only_fields = ('bidding', 'bidding_set',)

class BiddingImportedSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiddingImported
        fields = [
            'cnpj',
            'year',
            'seq',
        ]
    

class BiddingImportedHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = BiddingImported
        fields = [
            'id',
            'history_set',
        ]

class BiddingItemCompoundHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = BiddingItemCompound
        fields = [
            'id',
            'history_set',
        ]

class BiddingItemHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = BiddingItem
        fields = [
            'id',
            'history_set',
        ]

class BiddingFileHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = BiddingFile
        fields = [
            'id',
            'history_set',
        ]

class BiddingDetailHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = Bidding
        fields = [
            'id',
            'history_set',
        ]

class BiddingHistorySerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    def get_events(self, obj):
        result = []

        bidding_queryset = Bidding.objects.filter(id=obj.id)

        if bidding_queryset.exists():
            history = BiddingDetailHistorySerializer(bidding_queryset.first()).data
            for event in history['history_set']:
                result.append(event)

        file_queryset = BiddingFile.objects.filter(bidding=obj.id)

        if file_queryset.exists():
            for attach in file_queryset:
                history = BiddingFileHistorySerializer(attach).data
                for event in history['history_set']:
                    result.append(event)

        import_queryset = BiddingImported.objects.filter(bidding=obj.id)

        if import_queryset.exists():
            for attach in import_queryset:
                history = BiddingImportedHistorySerializer(attach).data
                for event in history['history_set']:
                    result.append(event)

        items_queryset = BiddingItem.objects.filter(bidding=obj.id)

        if items_queryset.exists():
            for item in items_queryset:
                history = BiddingItemHistorySerializer(item).data
                for event in history['history_set']:
                    result.append(event)

                product_queryset = BiddingItemCompound.objects.filter(item=item.id)
                if product_queryset.exists():
                    for prod in product_queryset:
                        history = BiddingItemCompoundHistorySerializer(prod).data
                        for event in history['history_set']:
                            result.append(event)

        filtered_result = []

        for event in result:
            if event['type'] == '~':
                if event['diff'] != None:
                    filtered_result.append(event)
            else:
                filtered_result.append(event)

        sort_result = sorted(filtered_result, key=lambda item:item['date'], reverse=True)
        return sort_result

    class Meta:
        model = Bidding
        fields = [
            'id',
            'events',
        ]

class BiddingItemTypeConvertSerializer(serializers.ModelSerializer):

    class Meta:
        model = BiddingItem
        fields = [
            'id',
            'type',
        ]
        
    def update(self, instance, validated_data):
        new_type = validated_data['type']
        instance_object = BiddingItem.objects.get(id=instance.id)
        serialized_item = BiddingItemSerializer(instance_object).data
        total_item_products = len(serialized_item['product_list'])

        if new_type == 'unit' and total_item_products > 1:
            message = "Can't convert to unit type with more than one product"
            raise serializers.ValidationError({ 'error': f"Fail to update bidding item: {message}" })
        

        instance.type = new_type
        instance.save()
        
        return instance

class BiddingToContractSerializer(serializers.ModelSerializer):
    client_set = ClientNameSerializer(source='client',
                                      read_only=True)

    class Meta:
        model = Bidding
        fields = [
            'id',
            'client',
            'client_set',
            'link_trade',
            'trade_number',
            'uasg',
        ]

class BiddingToAssistanceSerializer(serializers.ModelSerializer):
    client_set = ClientNamePhoneSerializer(source='client',
                                           read_only=True)

    class Meta:
        model = Bidding
        fields = [
            'id',
            'client',
            'client_set',
        ]
