from rest_framework import serializers
from django.db.models import Sum, F, DecimalField
from apps.utils.fields import FileBase64Field
from apps.utils.history import HistoryRecordField

from django_multitenant.utils import get_current_tenant

from .models import (
    Contract,
    ContractFilter,
    ContractType,
    ContractScope,
    ContractStatus,
    ContractFile,
    ContractItem,
    ContractItemCompound,
)

from apps.bidding.models import (
    Bidding,
    BiddingItem,
    BiddingItemCompound,
)

from apps.bidding.serializers import (
    BiddingToContractSerializer,
    BiddingToAssistanceSerializer,
)

from apps.client.serializers import (
    ClientSerializer,
    ClientNameSerializer,
)

from apps.accounts.serializers import (
    ProfileBasicSerializer,
)

from apps.product.serializers import (
    ProductSerializer,
    ProductToDeliverySerializer,
)

from apps.company.serializers import (
    CompanySerializer,
    CompanyNameSerializer,
)

from apps.order.serializers import (
    OrderCommitmentItem,
)

class ContractTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractType
        fields = [
            'id',
            'name',
        ]

class ContractScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractScope
        fields = [
            'id',
            'name',
        ]

class ContractStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractStatus
        fields = [
            'id',
            'name',
            'color',
            'initial',
        ]

class ContractFileSerializer(serializers.ModelSerializer):
    file = FileBase64Field(
        required=True,
        represent_in_base64=True,
        allow_null=True,
        allow_empty_file=True
    )

    class Meta:
        model = ContractFile
        fields = [
            'id',
            'file',
            'name',
            'contract',
        ]

class ContractFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractFile
        fields = [
            'id',
            'name',
        ]

class ContractSerializer(serializers.ModelSerializer):
    bidding_set = BiddingToContractSerializer(source='bidding',
                                              read_only=True)

    type_set = ContractTypeSerializer(source='type',
                                      read_only=True)

    scope_set = ContractScopeSerializer(source='scope',
                                      read_only=True)

    status_set = ContractStatusSerializer(source='status',
                                          read_only=True)

    owner_set = ProfileBasicSerializer(source='owner',
                                       read_only=True)

    file_set = ContractFileDetailSerializer(source='file',
                                            read_only=True,
                                            many=True)

    company = serializers.CharField(source='bidding.company.id',
                                    read_only=True)

    company_set = CompanyNameSerializer(source='bidding.company',
                                        read_only=True)

    is_outdated = serializers.SerializerMethodField()

    def get_is_outdated(self, obj):
        serializer_items = OutdatedContractItemSerializer(obj.items, many=True)

        for item in serializer_items.data:
            if item['is_cost_outdated']:
                return True

        return False

    class Meta:
        model = Contract
        fields = [
            'id',
            'bidding',
            'bidding_set',
            'status',
            'status_set',
            'scope',
            'scope_set',
            'type',
            'type_set',
            'date_start',
            'date_finish',
            'number',
            'observation',
            'owner',
            'owner_set',
            'state',
            'file_set',
            'email',
            'company',
            'company_set',
            'is_outdated',
        ]

        read_only_fields = ('company', 'company_set',)

    def create(self, validated_data):
        bidding = self.context['request'].data['bidding']

        isHomologated = False
        try:
            biddingModel = Bidding.objects.get(id=bidding)
            isHomologated = biddingModel.is_homologated
        except Exception as e:
            raise serializers.ValidationError("Fail to create contract, bidding was not found: Error: {exception}".format(exception=str(e)))

        if (not isHomologated):
            raise serializers.ValidationError("Fail to create contract, bidding is not homolagated")

        account = get_current_tenant()
        contractModel = Contract(account=account, **validated_data)
        try:
            contractModel.full_clean()
            contractModel.save()
        except Exception as e:
            raise serializers.ValidationError("Fail to create contract: Error: {exception}".format(exception=str(e)))

        contract = contractModel.id

        try:
            itemList = BiddingItem.objects.filter(bidding=bidding).order_by('-parent')

            for item in itemList:
                parent = None

                if ((item.type == 'lote')):
                    countItemGainInLote = BiddingItem.objects.filter(bidding=bidding, result='gain', parent=item.id).count()

                    if (countItemGainInLote == 0):
                        continue
                else:
                    if ((item.result != 'gain')):
                        continue

                if (item.parent):
                    parentModel = ContractItem.objects.filter(reference=item.parent)
                    parent = parentModel[0]

                contractItemModel = ContractItem(
                    contract=contractModel,
                    reference=item,
                    type=item.type,
                    parent=parent,
                    cost=item.cost,
                    name=item.name,
                    description=item.description,
                    number=item.number,
                    quantity=item.quantity,
                    fixed_cost=item.fixed_cost,
                    freight=item.freight,
                    fob_freight=item.fob_freight,
                    margin_min=item.margin_min,
                    price=item.price,
                    price_min=item.price_min,
                    tax=item.tax,
                    observation=item.observation,
                    account=account,
                )

                contractItemModel.full_clean()
                contractItemModel.save()

                itemCompoundList = BiddingItemCompound.objects.filter(item=item.id)

                for product in itemCompoundList:
                        ContractItemCompound.objects.create(
                                item=contractItemModel,
                                reference=product,
                                product=product.product,
                                quantity=product.quantity,
                                price=product.price,
                            )
        except Exception as e:
            contractModel.delete()
            raise serializers.ValidationError("Fail to create contract item: Error: {exception}".format(exception=str(e)))

        return contractModel

    def update(self, instance, validated_data):
        RELEASED_STATE = 'released'

        new_state = validated_data.get('state', instance.state)
        release_attempt = ((new_state == RELEASED_STATE) and (instance.state != RELEASED_STATE))
        released_bidding_contracts = Contract.objects.filter(bidding=instance.bidding, state=RELEASED_STATE) \
                                                      .exists()
        
        if (release_attempt and released_bidding_contracts):
            raise serializers.ValidationError(
                "Fail to update contract: Error: There are released contracts in this bidding"
            )
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

            return instance

    def to_representation(self, instance):
        instance = Contract.objects.select_related('bidding',
                                                     'status',
                                                     'type',
                                                     'scope',
                                                     'owner',
                                                     'bidding__client',
                                                     'bidding__company',
                                                    ).get(pk=instance.pk)

        return super().to_representation(instance)

class ContractListSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='bidding.client.id',
                                   read_only=True)
    
    client_set = ClientNameSerializer(source='bidding.client',
                                         read_only=True)

    company = serializers.CharField(source='bidding.company.id',
                                   read_only=True)

    company_set = CompanyNameSerializer(source='bidding.company',
                                  read_only=True)

    type_set = ContractTypeSerializer(source='type',
                                      read_only=True)
    
    status_set = ContractStatusSerializer(source='status',
                                  read_only=True)
    
    bidding_trade_number = serializers.CharField(source='bidding.trade_number',
                                                read_only=True)
    
    bidding_uasg = serializers.CharField(source='bidding.uasg',
                                        read_only=True)
    
    is_outdated = serializers.SerializerMethodField()

    def get_is_outdated(self, obj):
        serializer_items = OutdatedContractItemSerializer(obj.items, many=True)

        for item in serializer_items.data:
            if item['is_cost_outdated']:
                return True

        return False

    class Meta:
        model = Contract
        fields = [
            'id',
            'is_outdated',
            'client',
            'client_set',
            'company',
            'company_set',
            'type',
            'type_set',
            'number',
            'date_start',
            'date_finish',
            'status',
            'status_set',
            'state',
            'bidding_trade_number',
            'bidding_uasg',
        ]

class ContractToOrderSerializer(serializers.ModelSerializer):
    bidding_set = BiddingToContractSerializer(source='bidding',
                                              read_only=True)

    class Meta:
        model = Contract
        fields = [
            'id',
            'bidding',
            'bidding_set',
        ]

class ContractToAssistanceSerializer(serializers.ModelSerializer):
    bidding_set = BiddingToAssistanceSerializer(source='bidding',
                                                read_only=True)

    class Meta:
        model = Contract
        fields = [
            'id',
            'bidding',
            'bidding_set',
        ]


class ContractItemCompoundSerializer(serializers.ModelSerializer):
    product_set = ProductSerializer(source='product',
                                    read_only=True)

    class Meta:
        model = ContractItemCompound
        fields = [
            'id',
            'item',
            'product',
            'product_set',
            'price',
            'quantity',
        ]

class ContractItemCompoundToDeliverySerializer(serializers.ModelSerializer):
    product_set = ProductToDeliverySerializer(source='product',
                                            read_only=True)

    class Meta:
        model = ContractItemCompound
        fields = [
            'id',
            'item',
            'product',
            'product_set',
            'price',
            'quantity',
        ]

class ContractItemLoteSerializer(serializers.ModelSerializer):
    product_list = ContractItemCompoundSerializer(read_only=True,
                                                 many=True)
    class Meta:
        model = ContractItem
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
            'parent',
        ]

class ContractItemParentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractItem
        fields = [
            'id',
            'type',
            'name',
        ]

class ContractItemCommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractItem
        fields = [
            'id',
            'price',
        ]

class OutdatedContractItemSerializer(serializers.ModelSerializer):
    is_cost_outdated = serializers.SerializerMethodField()

    def get_is_cost_outdated(self, obj):
        result = False
        cost_contract = obj.cost

        if cost_contract:
            total_cost_qs = BiddingItemCompound.objects.filter(item=obj.reference).aggregate(
                total_cost=Sum(F('product__price'),
                output_field=DecimalField())
            )

            current_cost = total_cost_qs.get('total_cost', 0)

            delta = ((current_cost / cost_contract) - 1) * 100

            if delta > obj.contract.bidding.company.difference:
                result = True

        else:
            result = True

        return result 

    class Meta:
        model = ContractItem
        fields = [
            'id',
            'is_cost_outdated',
        ]

class ContractItemSerializer(serializers.ModelSerializer):
    product_list = ContractItemCompoundSerializer(read_only=True,
                                                 many=True)

    items_set = ContractItemLoteSerializer(source='items',
                                          read_only=True,
                                          many=True)

    parent_set = ContractItemParentDetailSerializer(source='parent',
                                                   read_only=True)

    is_cost_outdated = serializers.SerializerMethodField()

    def get_is_cost_outdated(self, obj):
        result = False
        cost_contract = obj.cost

        if cost_contract:
            total_cost_qs = BiddingItemCompound.objects.filter(item=obj.reference).aggregate(
                total_cost=Sum(F('product__price'),
                output_field=DecimalField())
            )

            current_cost = total_cost_qs.get('total_cost', 0)

            delta = ((current_cost / cost_contract) - 1) * 100

            if delta > obj.contract.bidding.company.difference:
                result = True

        else:
            result = True

        return result 

    class Meta:
        model = ContractItem
        fields = [
            'id',
            'contract',
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
            'parent',
            'parent_set',
            'items_set',
            'observation',
            'is_cost_outdated',
        ]

        read_only_fields = (
            'contract',
            'type',
            'product_list',
            'number',
            'name',
            'description',
            'price_min',
            'freight',
            'fob_freight',
            'tax',
            'fixed_cost',
            'margin_min',
            'parent',
            'observation',
        )

class ContractItemToDeliverySerializer(serializers.ModelSerializer):
    product_list = ContractItemCompoundToDeliverySerializer(read_only=True,
                                                            many=True)

    class Meta:
        model = ContractItem
        fields = [
            'id',
            'contract',
            'type',
            'product_list',
            'number',
            'name',
            'quantity',
            'cost',
            'price',
            'price_min',
            'freight',
            'tax',
            'fixed_cost',
            'parent',
        ]

        read_only_fields = (
            'contract',
            'type',
            'product_list',
            'number',
            'name',
            'price_min',
            'freight',
            'tax',
            'fixed_cost',
            'parent',
        )

class ContractItemsToCommitmentSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        item_to_commitment = []

        items_queryset = ContractItem.objects.filter(contract=obj, type__in=['unit', 'compound']) \
                                              .prefetch_related('ordercommitmentitem_set')

        for item in items_queryset:
            order_quantity = item.ordercommitmentitem_set.aggregate(
                total_quantity=Sum('quantity')
            )

            order_quantity = order_quantity.get('total_quantity') or 0

            balance = item.quantity - order_quantity

            result = {
                'balance': balance,
                'item': item.id,
                'item_set': ContractItemSerializer(item).data
            }

            item_to_commitment.append(result)

        return item_to_commitment

    class Meta:
        model = Contract
        fields = [
            'id',
            'items',
        ]

class ContractFilterSerializer(serializers.ModelSerializer):
    client_set = ClientSerializer(source='client',
                                  read_only=True)

    company_set = CompanySerializer(source='company',
                                    read_only=True)

    status_set = ContractStatusSerializer(source='status',
                                  read_only=True)

    type_set = ContractTypeSerializer(source='type',
                                      read_only=True)
    
    scope_set = ContractScopeSerializer(source='scope',
                                      read_only=True)

    class Meta:
        model = ContractFilter
        fields = [
            'id',
            'name',
            'client',
            'client_set',
            'company',
            'company_set',
            'status',
            'status_set',
            'type',
            'type_set',
            'scope',
            'scope_set',
            'date_start',
            'date_finish',
            'number',
            'is_outdated',
        ]

class ContractItemCompoundHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = ContractItemCompound
        fields = [
            'id',
            'history_set',
        ]

class ContractItemHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = ContractItem
        fields = [
            'id',
            'history_set',
        ]

class ContractFileHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = ContractFile
        fields = [
            'id',
            'history_set',
        ]

class ContractDetailHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = Contract
        fields = [
            'id',
            'history_set',
        ]

class ContractHistorySerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    def get_events(self, obj):
        result = []

        contract_queryset = Contract.objects.filter(id=obj.id)

        if contract_queryset.exists():
            history = ContractDetailHistorySerializer(contract_queryset.first()).data
            for event in history['history_set']:
                result.append(event)

        file_queryset = ContractFile.objects.filter(contract=obj.id)

        if file_queryset.exists():
            for attach in file_queryset:
                history = ContractFileHistorySerializer(attach).data
                for event in history['history_set']:
                    result.append(event)

        items_queryset = ContractItem.objects.filter(contract=obj.id)

        if items_queryset.exists():
            for item in items_queryset:
                history = ContractItemHistorySerializer(item).data
                for event in history['history_set']:
                    result.append(event)

                product_queryset = ContractItemCompound.objects.filter(item=item.id)
                if product_queryset.exists():
                    for prod in product_queryset:
                        history = ContractItemCompoundHistorySerializer(prod).data
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
        model = Contract
        fields = [
            'id',
            'events',
        ]

