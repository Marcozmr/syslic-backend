from rest_framework import serializers
from django.db.models import Subquery, Sum, F
from apps.utils.fields import FileBase64Field
from apps.utils.history import HistoryRecordField

from django_multitenant.utils import get_current_tenant

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
    OrderAssistanceStatus,
    OrderAssistanceType,
    OrderAssistance,
    OrderAssistanceFilter,
    OrderAuditPercentage,
    OrderInvoicingFilter,
    OrderInvoicingStatus,
    OrderInvoicingFile,
    OrderInvoicing,
)

from apps.bidding.models import (
    Bidding,
    BiddingItem,
    BiddingItemCompound,
)

from apps.commission.models import (
    Commission,
)

from apps.product.models import (
    Product,
)

from apps.product.serializers import (
    ProductSerializer,
    ProductBasicSerializer,
    ProductNameSerializer,
    ProductToAssistanceSerializer,
)

from apps.contract.models import (
    ContractItem,
    ContractItemCompound,
)

from apps.contract.serializers import (
    ContractSerializer,
    ContractToOrderSerializer,
    ContractToAssistanceSerializer,
    ContractItemSerializer,
    ContractItemToDeliverySerializer,
    ContractItemCompoundSerializer,
    ContractItemCommissionSerializer,
    ContractItemCompoundToDeliverySerializer,
)

from apps.company.serializers import (
    CompanySerializer,
    CompanyNameSerializer,
)

from apps.client.serializers import (
    ClientSerializer,
    ClientNameSerializer,
    ClientNameCNPJSerializer,
)

from apps.transport.serializers import (
    CarrierSerializer,
    CarrierNameSerializer,
    CarrierToDeliverySerializer,
)

from apps.accounts.serializers import (
    ProfileSerializer,
    ProfileToOrderListSerializer,
)

from apps.address.serializers import (
    CountrySerializer,
    StateSerializer,
    CitySerializer,
)

class OrderInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInterest
        fields = [
            'id',
            'name',
            'color',
        ]

class OrderFileSerializer(serializers.ModelSerializer):
    file = FileBase64Field(
        required=True,
        represent_in_base64=True,
        allow_null=True,
        allow_empty_file=True
    )

    class Meta:
        model = OrderFile
        fields = [
            'id',
            'file',
            'name',
            'order',
        ]

class OrderFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFile
        fields = [
            'id',
            'name',
        ]

class OrderSerializer(serializers.ModelSerializer):
    contract_set = ContractSerializer(source='contract',
                                    read_only=True)

    interest_set = OrderInterestSerializer(source='interest',
                                      read_only=True)

    company_set = CompanySerializer(source='company',
                                    read_only=True)

    owner_set = ProfileSerializer(source='owner',
                                 read_only=True)

    country_set = CountrySerializer(source='country',
                                    read_only=True)

    state_set = StateSerializer(source='state',
                                read_only=True)

    city_set = CitySerializer(source='city',
                              read_only=True)

    file_set = OrderFileDetailSerializer(source='file',
                                         read_only=True,
                                         many=True)

    price = serializers.SerializerMethodField()

    price_commitment = serializers.SerializerMethodField()

    has_delivery_done = serializers.SerializerMethodField()


    def get_price(self, obj):
        price = obj.contract.items \
                            .filter(
                                type__in=['unit', 'compound']
                            ) \
                            .aggregate(
                                total_price=Sum(
                                    F('quantity') * F('price')
                                )
                            ) \
                            .get('total_price', 0)

        return price


    def get_price_commitment(self, obj):
        price = OrderCommitmentItem.objects \
                                    .filter(
                                        item__contract=obj.contract,
                                        item__type__in=[
                                            'unit',
                                            'compound'
                                        ]
                                    ) \
                                    .aggregate(
                                        total_price=Sum(
                                            F('item__price') * F('quantity')
                                        )
                                    ) \
                                    .get('total_price', 0)

        return price

    def get_has_delivery_done(self, obj):
        has_delivery_done = False

        delivery_queryset = OrderDelivery.objects.filter(order=obj.id, situation='done')

        if delivery_queryset.exists():
            has_delivery_done = True

        return has_delivery_done

    class Meta:
        model = Order
        fields = [
            'id',
            'contract',
            'contract_set',
            'interest',
            'interest_set',
            'company',
            'company_set',
            'owner',
            'owner_set',
            'date_expiration',
            'address',
            'neighborhood',
            'number',
            'complement',
            'city',
            'city_set',
            'state',
            'state_set',
            'country',
            'country_set',
            'zip_code',
            'price',
            'price_commitment',
            'nf_payed',
            'file_set',
            'has_delivery_done',
        ]

class OrderListSerializer(serializers.ModelSerializer):
    contract_set = ContractToOrderSerializer(source='contract',
                                             read_only=True)

    interest_set = OrderInterestSerializer(source='interest',
                                      read_only=True)

    company_set = CompanyNameSerializer(source='company',
                                        read_only=True)

    owner_set = ProfileToOrderListSerializer(source='owner',
                                         read_only=True)

    price = serializers.SerializerMethodField()

    price_commitment = serializers.SerializerMethodField()


    def get_price(self, obj):
        price = obj.contract.items \
                            .filter(
                                type__in=['unit', 'compound']
                            ) \
                            .aggregate(
                                total_price=Sum(
                                    F('quantity') * F('price')
                                )
                            ) \
                            .get('total_price', 0)

        return price


    def get_price_commitment(self, obj):
        price = OrderCommitmentItem.objects \
                                    .filter(
                                        item__contract=obj.contract,
                                        item__type__in=[
                                            'unit',
                                            'compound'
                                        ]
                                    ) \
                                    .aggregate(
                                        total_price=Sum(
                                            F('item__price') * F('quantity')
                                        )
                                    ) \
                                    .get('total_price', 0)

        return price

    class Meta:
        model = Order
        fields = [
            'id',
            'contract',
            'contract_set',
            'interest',
            'interest_set',
            'company',
            'company_set',
            'owner',
            'owner_set',
            'date_expiration',
            'price',
            'price_commitment',
            'nf_payed',
        ]
class OrderToAssistanceSerializer(serializers.ModelSerializer):
    contract_set = ContractToAssistanceSerializer(source='contract',
                                                  read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'contract',
            'contract_set',
        ]

class OrderFilterSerializer(serializers.ModelSerializer):
    client_set = ClientSerializer(source='client',
                                  read_only=True)

    company_set = CompanySerializer(source='company',
                                    read_only=True)

    owner_set = ProfileSerializer(source='owner',
                                  read_only=True)
    
    interest_set = OrderInterestSerializer(source='interest',
                                      read_only=True)

    class Meta:
        model = OrderFilter
        fields = [
            'id',
            'name',
            'client',
            'client_set',
            'company',
            'company_set',
            'owner',
            'owner_set',
            'interest',
            'interest_set',
            'trade_number',
            'uasg',
            'nf_payed',
            'date_expiration_gte',
            'date_expiration_lte',
        ]

class OrderCommitmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCommitmentStatus
        fields = [
            'id',
            'name',
            'color',
            'initial',
        ]

class OrderCommitmentItemProductSerializer(serializers.ModelSerializer):
    product_set = ContractItemCompoundSerializer(source='product',
                                                read_only=True)


    class Meta:
        model = OrderCommitmentItemProduct
        fields = [
            'id',
            'item',
            'product',
            'product_set',
            'cost',
            'fob_freight',
            'last_audit_value',
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class OrderCommitmentItemProductToDeliverySerializer(serializers.ModelSerializer):
    product_set = ContractItemCompoundToDeliverySerializer(source='product',
                                                            read_only=True)


    class Meta:
        model = OrderCommitmentItemProduct
        fields = [
            'id',
            'item',
            'product',
            'product_set',
            'cost',
            'fob_freight',
            'last_audit_value',
        ]

class OrderCommitmentItemCommissionSerializer(serializers.ModelSerializer):
    contract_item = ContractItemCommissionSerializer(source='item',
                                                     read_only=True)
    class Meta:
        model = OrderCommitmentItem
        fields = [
            'id',
            'contract_item',
            'quantity',
        ]

class OrderCommitmentItemSerializer(serializers.ModelSerializer):
    contract_item = ContractItemSerializer(source='item',
                                         read_only=True)

    products_set = OrderCommitmentItemProductSerializer(source='products',
                                                        many=True,
                                                        read_only=True)

    class Meta:
        model = OrderCommitmentItem
        fields = [
            'id',
            'commitment',
            'item',
            'contract_item',
            'quantity',
            'annotation',
            'products',
            'products_set',
            'deliverable',
            'items_delivery',
            'last_audit_margin',
        ]
        read_only_fields = ('products', 'items_delivery')

    def create(self, validated_data):
        try:
            account = get_current_tenant()

            contract_item_serialized = ContractItemSerializer(validated_data['item']).data

            quantity_add_new_item = validated_data['quantity']
            quantity_max_item = contract_item_serialized['quantity']

            order_quantity = 0
            order_item_queryset = OrderCommitmentItem.objects.filter(commitment=validated_data['commitment'], item=validated_data['item'])
            for order_item in order_item_queryset:
                order_quantity += order_item.quantity

            available_quantity = quantity_max_item - order_quantity

            if available_quantity < quantity_add_new_item:
                raise serializers.ValidationError("The available quantity is less than the requested quantity.")

            item_model = OrderCommitmentItem(account=account, **validated_data)
            item_model.full_clean()
            item_model.save()

        except Exception as e:
            raise serializers.ValidationError("Fail to create order commitment item: Error: {exception}".format(exception=str(e)))

        try:
            contract_item = self.context['request'].data['item']
            product_list = ContractItemCompound.objects.filter(item=contract_item)

            for product in product_list:

                OrderCommitmentItemProduct.objects.create(item=item_model,
                                                          product=product,
                                                          cost=0)

        except Exception as e:
            item_model.delete()
            raise serializers.ValidationError("Fail to create order commitment item: Error: {exception}".format(exception=str(e)))

        return item_model

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if check_to_audit(instance.commitment.id):
            commitment = OrderCommitment.objects.get(id=instance.commitment.id)
            commitment.situation = 'audit'
            commitment.save()

        if(instance.commitment.situation == 'declined'):
            if (not check_to_audit(instance.commitment.id)):
                commitment = OrderCommitment.objects.get(id=instance.commitment.id)
                commitment.situation = 'idle'
                commitment.save()

        return instance

class OrderCommitmentItemToDeliverySerializer(serializers.ModelSerializer):
    contract_item = ContractItemToDeliverySerializer(source='item',
                                                    read_only=True)
    
    products_set = OrderCommitmentItemProductToDeliverySerializer(source='products',
                                                                    many=True,
                                                                    read_only=True)

    class Meta:
        model = OrderCommitmentItem
        fields = [
            'id',
            'commitment',
            'item',
            'contract_item',
            'quantity',
            'products',
            'products_set',
            'deliverable',
        ]

        read_only_fields = ('products', 'items_delivery')

class OrderCommitmentFileSerializer(serializers.ModelSerializer):
    file = FileBase64Field(
        required=True,
        represent_in_base64=True,
        allow_null=True,
        allow_empty_file=True
    )

    class Meta:
        model = OrderCommitmentFile
        fields = [
            'id',
            'file',
            'name',
            'commitment',
        ]

class OrderCommitmentFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCommitmentFile
        fields = [
            'id',
            'name',
        ]

class OrderCommitmentSerializer(serializers.ModelSerializer):
    bidding = serializers.CharField(source='order.contract.bidding.id',
                                    read_only=True)

    company_set = CompanyNameSerializer(source='company',
                                        read_only=True)

    status_set = OrderCommitmentStatusSerializer(source='status',
                                                 read_only=True)

    client = serializers.CharField(source='order.contract.bidding.client.id',
                                   read_only=True)

    client_set = ClientNameCNPJSerializer(source='order.contract.bidding.client',
                                  read_only=True)

    trade_number = serializers.CharField(source='order.contract.bidding.trade_number',
                                         read_only=True)

    file_set = OrderCommitmentFileDetailSerializer(source='file',
                                                   read_only=True,
                                                   many=True)

    price = serializers.SerializerMethodField()

    class Meta:
        model = OrderCommitment
        fields = [
            'id',
            'bidding',
            'order',
            'company',
            'company_set',
            'status',
            'status_set',
            'number',
            'date_delivery',
            'date_expiration',
            'items',
            'client',
            'client_set',
            'trade_number',
            'file_set',
            'price',
            'situation',
        ]

    def get_price(self, instance):
        items = instance.items.all()
        total = sum([item.item.price * item.quantity for item in items])

        return total
    
    def update(self, instance, validated_data):
        audit_percentages = OrderAuditPercentage.objects.first()
        commitment_percentage = (float(audit_percentages.delivery_percentage) / 100)

        for attr, value in validated_data.items():
            if attr == 'items' or attr == 'situation':
                continue
            setattr(instance, attr, value)

        instance.save()

        if commitment_percentage > 0 and instance.situation == 'idle':
            if check_to_audit(instance.id):

                instance.situation = 'audit'
                instance.save()


        if instance.situation == 'declined':
            if (not check_to_audit(instance.id)):
                instance.situation = 'idle'
                instance.save()
            

        return instance

class OrderCommitmentListSerializer(serializers.ModelSerializer):
    company_set = CompanyNameSerializer(source='company',
                                    read_only=True)

    status_set = OrderCommitmentStatusSerializer(source='status',
                                                 read_only=True)

    client = serializers.CharField(source='order.contract.bidding.client.id',
                                   read_only=True)

    client_set = ClientNameSerializer(source='order.contract.bidding.client',
                                  read_only=True)

    trade_number = serializers.CharField(source='order.contract.bidding.trade_number',
                                         read_only=True)
    
    price = serializers.SerializerMethodField()

    class Meta:
        model = OrderCommitment
        fields = [
            'id',
            'order',
            'company',
            'company_set',
            'status',
            'status_set',
            'number',
            'date_delivery',
            'date_expiration',
            'items',
            'client',
            'client_set',
            'trade_number',
            'situation',
            'price',
        ]

        read_only_fields = (
            'client',
            'client_set',
            'trade_number',
            'situation',
            'price'
        )

    def get_price(self, instance):
        items = instance.items.all()
        total = sum([item.item.price * item.quantity for item in items])

        return total

class OrderCommitmentToInvoicingListSerializer(serializers.ModelSerializer):
    client_set = ClientNameCNPJSerializer(source='order.contract.bidding.client',
                                      read_only=True)

    trade_number = serializers.CharField(source='order.contract.bidding.id',
                                    read_only=True)

    class Meta:
        model = OrderCommitment
        fields = [
            'id',
            'number',
            'client_set',
            'trade_number',
            'order',
        ]

def calculate_commitment_item_margin(commitment_item):
    contract_item_price = float(commitment_item['contract_item']['price'])
    contract_item_freight = float(commitment_item['contract_item']['freight'])
    contract_item_fixed_cost = float(commitment_item['contract_item']['fixed_cost'])

    product_list = commitment_item['products_set']

    unitary_cost = float(
        sum([(float(product['cost']) * int(product['product_set']['quantity'])) for product in product_list])
    )
    fob_freight = float(
        sum([float(product['fob_freight']) for product in product_list])
    )

    margin = contract_item_price - (fob_freight + unitary_cost
        + (contract_item_price * (contract_item_fixed_cost / 100))
        + (contract_item_price * (contract_item_freight / 100)))
    
    margin_percentage = round((margin / contract_item_price) * 100, 2)

    return margin_percentage

def check_to_audit(id):
    audit_percentages = OrderAuditPercentage.objects.first()
    commitment_item_percentage = float(audit_percentages.commitment_percentage)
    commitment_margin_percentage = float(audit_percentages.commitment_margin_percentage)
    
    items = OrderCommitmentItem.objects.filter(commitment=id)
    serialized_items = OrderCommitmentItemSerializer(items, many=True).data
        
    if serialized_items:
        for commitment_item in serialized_items:
            for commitment_product_item in commitment_item['products_set']:
                last_audit_value = float(commitment_product_item['last_audit_value'])
                last_audit_margin = float(commitment_item['last_audit_margin'])
                negotiated_value = float(commitment_product_item['cost'])
                item_price = float(commitment_product_item['product_set']['price'])

                max_value = (item_price + (item_price * (commitment_item_percentage / 100)))
                margin_percentage = calculate_commitment_item_margin(commitment_item)

                below_margin = (margin_percentage < commitment_margin_percentage) and (margin_percentage != last_audit_margin)
                exceeded_value = (negotiated_value > max_value) and (negotiated_value != last_audit_value)

                if below_margin or exceeded_value:
                    return True

    return False


class OrderCommitmentSituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCommitment
        fields = [
            'id',
            'situation',
        ]    
    
    def update(self, instance, validated_data):
        errors = []

        if (validated_data['situation'] == 'done'):
            item_queryset = OrderCommitmentItem.objects.filter(commitment=instance.id)
            not_has_item = False   
            is_undelivered_item = False   
            
            if len(item_queryset) > 0:
                for item_commitment in item_queryset:
                    count = 0
                    item_commitment_serializer = OrderCommitmentItemSerializer(item_commitment).data
                    item_delivery_queryset = OrderDeliveryItem.objects.filter(item=item_commitment)  
                    for item_delivery in item_delivery_queryset:
                        item_delivery_serializer = OrderDeliveryItemSerializer(item_delivery).data
                        count += item_delivery_serializer['quantity']

                    if not count == item_commitment_serializer['quantity']:
                        is_undelivered_item = True

                    delivery_queryset = OrderDelivery.objects.filter(items__in=item_delivery_queryset).exclude(situation='done')
                    if delivery_queryset.exists():
                        errors.append('there is incomplete delivery')
            else:
                not_has_item = True

            if not_has_item:
                errors.append('there is no item registered')

            if is_undelivered_item:
                errors.append('there is an undelivered item')


            if (len(errors) > 0):
                raise serializers.ValidationError({'errors': errors})
            
        elif (validated_data['situation'] == 'idle'):
            if (instance.situation == 'audit'):
                commitment_items = OrderCommitmentItem.objects.filter(commitment=instance.id)
                commitment_items_serializer = OrderCommitmentItemSerializer(commitment_items, many=True).data

                for item_commitment in commitment_items_serializer:
                    item_product_queryset = OrderCommitmentItemProduct.objects.filter(item=item_commitment['id'])

                    for item_product in item_product_queryset:                        
                        item_product_instance = OrderCommitmentItemProduct.objects.get(id=item_product.id)
                        item_product_instance.last_audit_value = item_product.cost
                        item_product_instance.save()

                    item_commitment_obj = OrderCommitmentItem.objects.get(id=item_commitment['id'])
                    item_commitment_obj.last_audit_margin = calculate_commitment_item_margin(item_commitment)
                    item_commitment_obj.save()

        elif (validated_data['situation'] == 'declined'):
            commitment_items = OrderCommitmentItem.objects.filter(commitment=instance.id)
            commitment_items_serializer = OrderCommitmentItemSerializer(commitment_items, many=True).data

            for item_commitment in commitment_items_serializer:
                item_product_queryset = OrderCommitmentItemProduct.objects.filter(item=item_commitment['id'])

                for item_product in item_product_queryset:
                    item_product_instance = OrderCommitmentItemProduct.objects.get(id=item_product.id)            
                    item_product_instance.last_audit_value = 0
                    item_product_instance.save()

                item_commitment_obj = OrderCommitmentItem.objects.get(id=item_commitment['id'])
                item_commitment_obj.last_audit_margin = 0
                item_commitment_obj.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    


class OrderCommitmentFilterSerializer(serializers.ModelSerializer):
    status_set = OrderCommitmentStatusSerializer(source='status',
                                                 read_only=True)

    client_set = ClientSerializer(source='client',
                                  read_only=True)
    class Meta:
        model = OrderCommitmentFilter
        fields = [
            'id',
            'name',
            'status',
            'status_set',
            'number',
            'date_delivery',
            'date_expiration',
            'client',
            'client_set',
            'trade_number',
            'note_number',
            'billing_date',
            'pay_date',
            'real_pay_date',
        ]
        
class OrderItemsToCommitmentSerializer(serializers.ModelSerializer):
    items_to_commitment = serializers.SerializerMethodField()

    items_from_commitment = serializers.SerializerMethodField()

    items_from_contract = ContractItemSerializer(source='contract.items',
                                                 read_only=True,
                                                 many=True)

    def get_items_from_commitment(self, obj):
        commitment_queryset = OrderCommitment.objects.filter(order=obj.id)

        if commitment_queryset:
            result = OrderCommitmentItem.objects.filter(commitment__in=commitment_queryset)
            if result:
                serializer = OrderCommitmentItemSerializer(result, many=True)
                return serializer.data

        return None

    def get_items_to_commitment(self, obj):
        items_queryset = ContractItem.objects.filter(contract=obj.contract, type__in=['unit', 'compound'])

        item_to_commitment = []

        for item in items_queryset:
            order_quantity = 0
            order_item_queryset = OrderCommitmentItem.objects.filter(item=item.id)
            for order_item in order_item_queryset:
                order_quantity += order_item.quantity

            quantity = item.quantity - order_quantity

            result = {
                'quantity': quantity,
                'item': item.id,
                'item_set': ContractItemSerializer(item).data
            }

            item_to_commitment.append(result)

        return item_to_commitment

    class Meta:
        model = Order
        fields = [
            'id',
            'items_to_commitment',
            'items_from_commitment',
            'items_from_contract',
        ]

class OrderItemsReportSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        items_queryset = ContractItem.objects.filter(contract=obj.contract, type__in=['unit', 'compound'])

        items_report = []

        for item in items_queryset:
            commitment_quantity = 0
            delivery_quantity = 0

            commitment_queryset = OrderCommitmentItem.objects.filter(item=item.id)
            for commitment_item in commitment_queryset:
                commitment_quantity += commitment_item.quantity

            commitment_item_list = commitment_queryset.values_list('id', flat=True)

            delivery_queryset = OrderDeliveryItem.objects.filter(item__in=Subquery(commitment_item_list))
            for delivery_item in delivery_queryset:
                delivery_quantity += delivery_item.quantity

            quantity = item.quantity - commitment_quantity

            result = {
                'item': item.id,
                'item_set': ContractItemSerializer(item).data,
                'quantity' : {
                    'avaiable': quantity,
                    'commitment': commitment_quantity,
                    'delivery': delivery_quantity,
                }
            }

            items_report.append(result)

        return items_report

    class Meta:
        model = Order
        fields = [
            'id',
            'items',
        ]

class OrderDeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDeliveryStatus
        fields = [
            'id',
            'name',
            'color',
            'initial',
        ]

class OrderDeliveryFileSerializer(serializers.ModelSerializer):
    file = FileBase64Field(
        required=True,
        represent_in_base64=True,
        allow_null=True,
        allow_empty_file=True
    )

    class Meta:
        model = OrderDeliveryFile
        fields = [
            'id',
            'file',
            'name',
            'delivery',
        ]

class OrderDeliveryFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDeliveryFile
        fields = [
            'id',
            'name',
        ]

class OrderDeliveryItemSerializer(serializers.ModelSerializer):
    item_set = OrderCommitmentItemToDeliverySerializer(source='item',
                                                     read_only=True)

    class Meta:
        model = OrderDeliveryItem
        fields = [
            'id',
            'delivery',
            'item',
            'item_set',
            'quantity',
        ]

class OrderDeliveryFreightCotationSerializer(serializers.ModelSerializer):
    carrier_set = CarrierToDeliverySerializer(source='carrier',
                                             read_only=True)

    class Meta:
        model = OrderDeliveryFreightCotation
        fields = [
            'id',
            'delivery',
            'carrier',
            'carrier_set',
            'email',
            'phone_number',
            'cost',
            'date_cotation',
            'accepted',
            'quote_number',
        ]

    def save_related_invoicings(self, instance):
        invoicing_queryset = OrderInvoicing.objects.filter(delivery=instance.delivery.id)

        if invoicing_queryset.exists():
            for invoicing in invoicing_queryset:
                invoicing.save()

    def create(self, validated_data):
        instance = OrderDeliveryFreightCotation.objects.create(**validated_data)

        self.save_related_invoicings(instance)

        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        self.save_related_invoicings(instance)

        return instance

class OrderDeliverySerializer(serializers.ModelSerializer):
    bidding = serializers.CharField(source='order.contract.bidding.id',
                                    read_only=True)

    status_set = OrderDeliveryStatusSerializer(source='status',
                                               read_only=True)

    company_set = CompanyNameSerializer(source='company',
                                        read_only=True)

    client = serializers.CharField(source='order.contract.bidding.client.id',
                                   read_only=True)

    client_set = ClientNameCNPJSerializer(source='order.contract.bidding.client',
                                          read_only=True)

    carrier_set = CarrierNameSerializer(source='carrier',
                                        read_only=True)

    file_set = OrderDeliveryFileDetailSerializer(source='file',
                                                 read_only=True,
                                                 many=True)    

    cotations_set = OrderDeliveryFreightCotationSerializer(source='cotations',
                                                           read_only=True,
                                                           many=True)

    city_set = CitySerializer(source='city',
                                read_only=True)
    
    state_set = StateSerializer(source='state',
                                read_only=True)
    
    country_set = CountrySerializer(source='country',
                                    read_only=True)

    trade_number = serializers.CharField(source='order.contract.bidding.trade_number',
                                         read_only=True)

    freight_estimated = serializers.DecimalField(max_digits=20,
                                                 decimal_places=2,
                                                 default=0,
                                                 read_only=True)

    freight_real = serializers.DecimalField(max_digits=20,
                                            decimal_places=2,
                                            default=0,
                                            read_only=True)

    total_value = serializers.DecimalField(max_digits=20,
                                           decimal_places=2,
                                           default=0,
                                           read_only=True)

    class Meta:
        model = OrderDelivery
        fields = [
            'id',
            'order',
            'bidding',
            'company',
            'company_set',
            'client',
            'client_set',
            'status',
            'status_set',
            'date_delivery',
            'carrier',
            'carrier_set',
            'freight_cost',
            'annotation',
            'address',
            'neighborhood',
            'number',
            'complement',
            'city',
            'city_set',
            'situation',
            'state',
            'state_set',
            'country',
            'country_set',
            'zip_code',
            'file_set',
            'items',
            'cotations',
            'cotations_set',
            'trade_number',
            'expedition_date',
            'invoicing_delivery_date',
            'driver_name',
            'freight_estimated',
            'freight_real',
            'total_value',
            'last_audit_value',
        ]

        read_only_fields = (
            'items',
            'cotations',
            'freight_estimated',
            'freight_real',
            'total_value',
        )

    def save_related_invoicings(self, instance):
        invoicing_queryset = OrderInvoicing.objects.filter(delivery=instance.id)

        if invoicing_queryset.exists():
            for invoicing in invoicing_queryset:
                invoicing.save()                

    def update(self, instance, validated_data):
        delivery = OrderDelivery.objects.filter(id=instance.id).annotate(
            freight_estimated = Sum(F('items__item__item__price') * F('items__quantity') * (F('items__item__item__freight')/100), distinct=True),
            total_value = Sum(F('items__item__item__price') * F('items__quantity'), distinct=True),
            freight_real = Sum(F('cotations__cost'), filter=F('cotations__accepted'), distinct=True),
        ).first()

        new_situation = validated_data.get('situation', None)

        if new_situation == 'done':
            if instance.situation != 'released':
                raise serializers.ValidationError({'situation': 'Refresh the page to load the current delivery situation.'})
        
        if instance.situation == 'done':
            if new_situation and new_situation == 'idle':
                delivery_items_queryset = OrderDeliveryItem.objects.filter(delivery=instance.id)
                
                if delivery_items_queryset.exists():
                    for delivery_item in delivery_items_queryset:
                        commitment_item = OrderCommitmentItem.objects.get(id=delivery_item.item.id)
                        commitment = OrderCommitment.objects.get(id=commitment_item.commitment.id)
                        if commitment.situation == 'done':
                            raise serializers.ValidationError({'commitment': 'this delivery is linked to a closed commitment.'})
        
        audit_percentages = OrderAuditPercentage.objects.first()
        delivery_percentage = (float(audit_percentages.delivery_percentage) / 100) or 0

        estimated_freight = delivery.freight_estimated
        estimated_freight = float(estimated_freight) if estimated_freight else 0

        max_freight_value = round((estimated_freight + (estimated_freight * delivery_percentage)), 2)
        last_audit_value = float(instance.last_audit_value)

        delivery_cotation_set = self.context['request'].data.get('cotations_set', None)

        if delivery_cotation_set:
            for cotation in delivery_cotation_set:
                if cotation['accepted']:
                    freight = float(cotation['cost'])

                    if freight > max_freight_value and freight != last_audit_value:
                        for attr, value in validated_data.items():
                            setattr(instance, attr, value)

                        instance.situation = 'audit'
                        instance.save()
                        self.save_related_invoicings(instance)

                        return instance
                            
        if instance.situation == 'declined':
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.situation = 'idle'
            instance.save()
            self.save_related_invoicings(instance)
            
            return instance

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        self.save_related_invoicings(instance)

        return instance

class OrderDeliveryListSerializer(serializers.ModelSerializer):    
    client = serializers.CharField(source='order.contract.bidding.client.id',
                                   read_only=True)

    client_set = ClientNameSerializer(source='order.contract.bidding.client',
                                      read_only=True)
    
    trade_number = serializers.CharField(source='order.contract.bidding.trade_number',
                                         read_only=True)
    
    company_set = CompanyNameSerializer(source='company',
                                        read_only=True)

    carrier_set = CarrierNameSerializer(source='carrier',
                                        read_only=True)
    
    status_set = OrderDeliveryStatusSerializer(source='status',
                                               read_only=True)

    freight_estimated = serializers.DecimalField(max_digits=20,
                                                 decimal_places=2,
                                                 default=0,
                                                 read_only=True)

    freight_real = serializers.DecimalField(max_digits=20,
                                            decimal_places=2,
                                            default=0,
                                            read_only=True)

    total_value = serializers.DecimalField(max_digits=20,
                                           decimal_places=2,
                                           default=0,
                                           read_only=True)
    
    class Meta:
        model = OrderDelivery
        fields = [
            'id',
            'order',
            'company',
            'company_set',
            'client',
            'client_set',
            'status',
            'status_set',
            'date_delivery',
            'carrier',
            'carrier_set',
            'freight_cost',
            'situation',            
            'items',
            'cotations',
            'trade_number',
            'invoicing_delivery_date',
            'driver_name',
            'freight_estimated',
            'freight_real',
            'total_value',
            'last_audit_value',
        ]

        read_only_fields = (
            'items',
            'cotations',
            'freight_estimated',
            'freight_real',
            'total_value',
        )

class OrderDeliveryToInvoicingListSerializer(serializers.ModelSerializer):
    company_set = CompanyNameSerializer(source='company',
                                        read_only=True)

    class Meta:
        model = OrderDelivery
        fields = [
            'id',
            'company',
            'company_set',
            'date_delivery',
            'invoicing_delivery_date',
        ]

class OrderDeliveryToInvoicingViewSerializer(serializers.ModelSerializer):
    company_set = CompanyNameSerializer(source='company',
                                        read_only=True)

    client_set = ClientNameCNPJSerializer(source='order.contract.bidding.client',
                                          read_only=True)

    class Meta:
        model = OrderDelivery
        fields = [
            'id',
            'company',
            'company_set',
            'client_set',
            'date_delivery',
            'invoicing_delivery_date',
            'order',
        ]

class OrderItemsToDeliverySerializer(serializers.ModelSerializer):
    items_to_delivery = serializers.SerializerMethodField()

    def get_commitment_list(self, obj):
        UNAVALIABLE_SITUATIONS = [
            'audit',
            'declined'
        ]

        return OrderCommitment.objects.filter(order=obj.order.id) \
                                        .exclude(situation__in=UNAVALIABLE_SITUATIONS)

    def get_items_to_delivery(self, obj):
        commitment_queryset = self.get_commitment_list(obj)

        items_to_delivery = []

        if commitment_queryset:
            for commitment in commitment_queryset:
                items_qs = OrderCommitmentItem.objects.filter(commitment=commitment.id,
                                                              deliverable=True)

                result = {
                    'commitment': commitment.id,
                    'commitment_set': OrderCommitmentSerializer(commitment).data,
                    'quantity': 0,
                    'items': [],
                }
                
                if items_qs:
                    for item in items_qs:
                        delivery_quantity = 0
                        delivery_item_queryset = OrderDeliveryItem.objects.filter(item=item.id)

                        for delivery_item in delivery_item_queryset:
                            delivery_quantity += delivery_item.quantity

                        quantity = item.quantity - delivery_quantity

                        item = {
                            'quantity': quantity,
                            'item': item.id,
                            'item_set': OrderCommitmentItemSerializer(item).data
                        }

                        result['quantity'] += quantity

                        result['items'].append(item)

                    items_to_delivery.append(result)
                    
        return items_to_delivery

    class Meta:
        model = OrderDelivery
        fields = [
            'id',
            'items_to_delivery',
        ]

class OrderDeliveryFilterSerializer(serializers.ModelSerializer):
    client_set = ClientSerializer(source='client',
                                  read_only=True)

    company_set = CompanySerializer(source='company',
                                    read_only=True)

    carrier_set = CarrierSerializer(source='carrier',
                                    read_only=True)
    
    status_set = OrderDeliveryStatusSerializer(source='status',
                                               read_only=True)

    class Meta:
        model = OrderDeliveryFilter
        fields = [
            'id',
            'name',
            'delivery_number',
            'client',
            'client_set',
            'trade_number',
            'company',
            'company_set',
            'carrier',
            'carrier_set',
            'status',
            'status_set',
            'date_delivery',
            'invoicing_delivery_date',
        ]

class OrderFileHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = OrderFile
        fields = [
            'id',
            'history_set',
        ]

class OrderDetailHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'history_set',
        ]

class OrderHistorySerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    def get_events(self, obj):
        result = []

        order_queryset = Order.objects.filter(id=obj.id)

        if order_queryset.exists():
            history = OrderDetailHistorySerializer(order_queryset.first()).data
            for event in history['history_set']:
                result.append(event)

        file_queryset = OrderFile.objects.filter(order=obj.id)

        if file_queryset.exists():
            for attach in file_queryset:
                history = OrderFileHistorySerializer(attach).data
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
        model = Order
        fields = [
            'id',
            'events',
        ]

class OrderCommitmentItemProductHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = OrderCommitmentItemProduct
        fields = [
            'id',
            'history_set',
        ]

class OrderCommitmentItemHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = OrderCommitmentItem
        fields = [
            'id',
            'history_set',
        ]

class OrderCommitmentFileHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = OrderCommitmentFile
        fields = [
            'id',
            'history_set',
        ]

class OrderCommitmentDetailHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = OrderCommitment
        fields = [
            'id',
            'history_set',
        ]

class OrderCommitmentHistorySerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    def get_events(self, obj):
        result = []

        commitment_queryset = OrderCommitment.objects.filter(id=obj.id)

        if commitment_queryset.exists():
            history = OrderCommitmentDetailHistorySerializer(commitment_queryset.first()).data
            for event in history['history_set']:
                result.append(event)

        file_queryset = OrderCommitmentFile.objects.filter(commitment=obj.id)

        if file_queryset.exists():
            for attach in file_queryset:
                history = OrderCommitmentFileHistorySerializer(attach).data
                for event in history['history_set']:
                    result.append(event)

        items_queryset = OrderCommitmentItem.objects.filter(commitment=obj.id)

        if items_queryset.exists():
            for item in items_queryset:
                history = OrderCommitmentItemHistorySerializer(item).data
                for event in history['history_set']:
                    result.append(event)

                product_queryset = OrderCommitmentItemProduct.objects.filter(item=item.id)
                if product_queryset.exists():
                    for prod in product_queryset:
                        history = OrderCommitmentItemProductHistorySerializer(prod).data
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
        model = OrderCommitment
        fields = [
            'id',
            'events',
        ]

class OrderDeliveryFreightCotationHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = OrderDeliveryFreightCotation
        fields = [
            'id',
            'history_set',
        ]

class OrderDeliveryFileHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = OrderDeliveryFile
        fields = [
            'id',
            'history_set',
        ]

class OrderDeliveryItemHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = OrderDeliveryItem
        fields = [
            'id',
            'history_set',
        ]

class OrderDeliveryDetailHistorySerializer(serializers.ModelSerializer):
    history_set = HistoryRecordField(source='history', read_only=True)

    class Meta:
        model = OrderDelivery
        fields = [
            'id',
            'history_set',
        ]

class OrderDeliveryHistorySerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    def get_events(self, obj):
        result = []

        delivery_queryset = OrderDelivery.objects.filter(id=obj.id)

        if delivery_queryset.exists():
            history = OrderDeliveryDetailHistorySerializer(delivery_queryset.first()).data
            for event in history['history_set']:
                result.append(event)

        items_queryset = OrderDeliveryItem.objects.filter(delivery=obj.id)

        if items_queryset.exists():
            for item in items_queryset:
                history = OrderDeliveryItemHistorySerializer(item).data
                for event in history['history_set']:
                    result.append(event)

        file_queryset = OrderDeliveryFile.objects.filter(delivery=obj.id)

        if file_queryset.exists():
            for doc in file_queryset:
                history = OrderDeliveryFileHistorySerializer(doc).data
                for event in history['history_set']:
                    result.append(event)

        freight_queryset = OrderDeliveryFreightCotation.objects.filter(delivery=obj.id)

        if freight_queryset.exists():
            for freight in freight_queryset:
                history = OrderDeliveryFreightCotationHistorySerializer(freight).data
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
        model = OrderDelivery
        fields = [
            'id',
            'events',
        ]

class OrderAssistanceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAssistanceStatus
        fields = [
            'id',
            'name',
            'color',
        ]
        
class OrderAssistanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAssistanceType
        fields = [
            'id',
            'name',
        ]
        
class OrderAssistanceSerializer(serializers.ModelSerializer):
    order_set = OrderSerializer(source='order',
                                read_only=True)
    
    status_set = OrderAssistanceStatusSerializer(source='status',
                                                 read_only=True)
    
    type_set = OrderAssistanceTypeSerializer(source='type',
                                             read_only=True)
    
    product_set = ProductSerializer(source='product',
                                    read_only=True)
    
    class Meta:
        model = OrderAssistance
        fields = [
            'id',
            'order',
            'order_set',
            'product',
            'product_set',
            'type',
            'type_set',
            'status',
            'status_set',
            'organ_phone',
            'date_scheduled',
            'comments',
            'payment_value',
            'technician_name',
            'technician_phone',
        ]

class OrderAssistanceListSerializer(serializers.ModelSerializer):
    order_set = OrderToAssistanceSerializer(source='order',
                                           read_only=True)
    
    product_set = ProductToAssistanceSerializer(source='product',
                                                read_only=True)

    type_set = OrderAssistanceTypeSerializer(source='type',
                                             read_only=True)
    
    status_set = OrderAssistanceStatusSerializer(source='status',
                                                read_only=True)

    
    class Meta:
        model = OrderAssistance
        fields = [
            'id',
            'order',
            'order_set',
            'product',
            'product_set',
            'type',
            'type_set',
            'status',
            'status_set',
            'organ_phone',
            'date_scheduled',
            'comments',
            'payment_value',
            'technician_name',
            'technician_phone',
        ]

class OrderAssistanceBasicSerializer(serializers.ModelSerializer):
    order_set = OrderToAssistanceSerializer(source='order',
                                           read_only=True)
    
    product_set = ProductNameSerializer(source='product',
                                        read_only=True)

    type_set = OrderAssistanceTypeSerializer(source='type',
                                             read_only=True)
    
    status_set = OrderAssistanceStatusSerializer(source='status',
                                                read_only=True)

    
    class Meta:
        model = OrderAssistance
        fields = [
            'id',
            'order',
            'order_set',
            'product',
            'product_set',
            'type',
            'type_set',
            'status',
            'status_set',
            'organ_phone',
            'date_scheduled',
            'comments',
            'payment_value',
            'technician_name',
            'technician_phone',
        ]
        
class OrderAssistanceFilterSerializer(serializers.ModelSerializer):
    client_set = ClientSerializer(source='client',
                                  read_only=True)
    
    type_set = OrderAssistanceTypeSerializer(source='type',
                                            read_only=True)

    status_set = OrderAssistanceStatusSerializer(source='status',
                                                read_only=True)

    class Meta:
        model = OrderAssistanceFilter
        fields = [
            'id',
            'name',
            'client',
            'client_set',
            'type',
            'type_set',
            'status',
            'status_set',
            'date_scheduled_gte',
            'date_scheduled_lte',
        ]

class OrderProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, obj):
        bidding_queryset = Bidding.objects.filter(id=obj.contract.bidding.id)

        if bidding_queryset.exists():
            biddingitem_queryset = BiddingItem.objects.filter(bidding__in=bidding_queryset)
            if biddingitem_queryset.exists():
                biddingitem_compound_queryset = BiddingItemCompound.objects.filter(item__in=biddingitem_queryset)
                products_id = []
                for product in biddingitem_compound_queryset:
                    products_id.append(product.product.id)
                
                product_queryset = Product.objects.filter(id__in=products_id)
                products = ProductBasicSerializer(product_queryset, many=True)
                return products.data

        return []

    class Meta:
        model = Order
        fields = [
            'id',
            'products',
        ]

class OrderAuditPercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAuditPercentage
        fields = [
            'id',
            'commitment_percentage',
            'delivery_percentage',
            'commitment_margin_percentage',
        ]

class OrderDeliverySituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDelivery
        fields = [
            'id',
            'situation',
        ]

    def update(self, instance, validated_data):
        new_situation = validated_data['situation']
        
        if new_situation in ('idle', 'invoicing', 'released'):
            if instance.situation == 'audit':
                delivery_cotations = OrderDeliveryFreightCotation.objects.filter(delivery=instance.id)
                if delivery_cotations.exists():
                    for cotation in delivery_cotations:
                        if cotation.accepted:
                            instance.last_audit_value = cotation.cost
                            instance.situation = new_situation
                            instance.save()

                            return instance
                        
        if new_situation == 'declined':
            instance.last_audit_value = 0
            instance.situation = new_situation
            instance.save()
            
            return instance
        
        instance.save()
        return instance

class OrderInvoicingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInvoicingStatus
        fields = [
            'id',
            'name',
            'color',
            'initial',
        ]

class OrderInvoicingFileSerializer(serializers.ModelSerializer):
    file = FileBase64Field(
        required=True,
        represent_in_base64=True,
        allow_null=True,
        allow_empty_file=True
    )

    class Meta:
        model = OrderInvoicingFile
        fields = [
            'id',
            'file',
            'name',
            'invoicing',
        ]

class OrderInvoicingFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInvoicingFile
        fields = [
            'id',
            'name',
        ]

class OrderInvoicingSerializer(serializers.ModelSerializer):
    delivery_set = OrderDeliverySerializer(source='delivery',
                                           read_only=True)

    commitment_set = OrderCommitmentSerializer(source='commitment',
                                           read_only=True)

    status_set = OrderInvoicingStatusSerializer(source='status',
                                                read_only=True)

    file_set = OrderInvoicingFileDetailSerializer(source='file',
                                                  read_only=True,
                                                  many=True)

    class Meta:
        model = OrderInvoicing
        fields = [
            'id',
            'delivery',
            'delivery_set',
            'commitment',
            'commitment_set',
            'note_number',
            'invoicing_date',
            'expected_payment_date',
            'real_pay_date',
            'annotation',
            'status',
            'status_set',
            'file_set',
            'total_nf',
            'liquid_margin',
            'situation',
        ]

        read_only_fields = ('delivery', 'situation', 'total_nf', 'liquid_margin')

class OrderInvoicingListSerializer(serializers.ModelSerializer):
    delivery_set = OrderDeliveryToInvoicingListSerializer(source='delivery',
                                                      read_only=True)

    commitment_set = OrderCommitmentToInvoicingListSerializer(source='commitment',
                                                              read_only=True)

    status_set = OrderInvoicingStatusSerializer(source='status',
                                                read_only=True)

    class Meta:
        model = OrderInvoicing
        fields = [
            'id',
            'delivery',
            'delivery_set',
            'commitment',
            'commitment_set',
            'note_number',
            'real_pay_date',
            'status',
            'status_set',
            'total_nf',
            'liquid_margin',
            'situation',
        ]

        read_only_fields = ('delivery', 'situation')

class OrderInvoicingViewSerializer(serializers.ModelSerializer):
    delivery_set = OrderDeliveryToInvoicingViewSerializer(source='delivery',
                                                      read_only=True)

    commitment_set = OrderCommitmentToInvoicingListSerializer(source='commitment',
                                                              read_only=True)

    status_set = OrderInvoicingStatusSerializer(source='status',
                                                read_only=True)

    file_set = OrderInvoicingFileDetailSerializer(source='file',
                                                  read_only=True,
                                                  many=True)

    bidding = serializers.CharField(source='delivery.order.contract.bidding.id',
                                    read_only=True)

    class Meta:
        model = OrderInvoicing
        fields = [
            'id',
            'delivery',
            'delivery_set',
            'commitment',
            'commitment_set',
            'note_number',
            'invoicing_date',
            'expected_payment_date',
            'real_pay_date',
            'annotation',
            'status',
            'status_set',
            'file_set',
            'total_nf',
            'liquid_margin',
            'situation',
            'bidding',
        ]

class OrderInvoicingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInvoicing
        fields = [
            'delivery',
        ]

    def create(self, validated_data):
        try:
            invoicing_status_list = OrderInvoicingStatus.objects.filter(initial=True)

            if invoicing_status_list.exists():
                invoicing_status = invoicing_status_list.first()
            else:
                raise serializers.ValidationError('There is no initial status for the invoicing')

        except Exception as e:
            raise serializers.ValidationError("Fail to create order invoicing: Error: {exception}".format(exception=str(e)))

        try:
            delivery = OrderDeliverySerializer(validated_data['delivery'])
            items_queryset = OrderDeliveryItem.objects.filter(delivery=delivery['id'].value)
            for item in items_queryset:
                items_serializer = OrderDeliveryItemSerializer(item).data
                item_commitment = OrderCommitmentItem.objects.filter(id=items_serializer['item'])

                item_commitment_serializer = OrderCommitmentItemSerializer(item_commitment.first()).data
                commitment_queryset = OrderCommitment.objects.filter(id=item_commitment_serializer['commitment'])
                commitment = commitment_queryset.first()

                invoicing_queryset = OrderInvoicing.objects.filter(commitment=commitment, delivery=delivery['id'].value)
                if not invoicing_queryset.exists():
                    account = get_current_tenant()
                    invoicing_model = OrderInvoicing(**validated_data, status=invoicing_status, commitment=commitment, account=account)
                    invoicing_model.save()

        except Exception as e:
            raise serializers.ValidationError("Fail to create order invoicing: Error: {exception}".format(exception=str(e)))

        return invoicing_model

class OrderInvoicingSituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInvoicing
        fields = [
            'id',
            'situation',
        ]
    
    def update(self, instance, validated_data):
        errors = []

        if (validated_data['situation'] == 'released'):
            if (instance.situation == 'idle'):
                if (instance.note_number == '' or instance.note_number is None):
                    errors.append('note_number is required')
                
                if instance.expected_payment_date is None:
                    errors.append('expected_payment_date is required')

                invoicing_files_queryset = OrderInvoicingFile.objects.filter(invoicing=instance.id)
                if not invoicing_files_queryset.exists():
                    errors.append('there is no attachment added')

            elif (instance.situation == 'done'):
                commission_queryset = Commission.objects.filter(invoicing=instance.id, status__in=['payed', 'pending'])
                if commission_queryset.exists():
                    errors.append('there are comisssions payed')

            if (len(errors) > 0):
                raise serializers.ValidationError({'errors': errors})
            else:
                invoicing_list = OrderInvoicing.objects.filter(delivery=instance.delivery, situation='idle').exclude(id=instance.id)
                
                delivery_serializer = OrderDeliverySerializer(instance.delivery).data
                if not invoicing_list.exists() and delivery_serializer['situation'] == 'invoicing':
                    invoicing_delivery = OrderDelivery.objects.get(id=instance.delivery.id)

                    invoicing_delivery.situation = 'released'
                    invoicing_delivery.save()
            
        elif (validated_data['situation'] == 'idle'):
            delivery_serializer = OrderDeliverySerializer(instance.delivery).data
            if delivery_serializer['situation'] == 'done':
                errors.append('delivery of this invoicing is complete')
            else:
                delivery_serializer = OrderDeliverySerializer(instance.delivery).data
                if delivery_serializer['situation'] == 'released':
                    invoicing_delivery = OrderDelivery.objects.get(id=instance.delivery.id)

                    invoicing_delivery.situation = 'invoicing'
                    invoicing_delivery.save()

            if (len(errors) > 0):
                raise serializers.ValidationError({'errors': errors})

        elif (validated_data['situation'] == 'done'):
            if (instance.note_number == '' or instance.note_number is None):
                errors.append('note_number is required')

            if instance.invoicing_date is None:
                errors.append('invoicing_date is required')
            
            if instance.expected_payment_date is None:
                errors.append('expected_payment_date is required')

            if instance.real_pay_date is None:
                errors.append('real_pay_date is required')

            invoicing_files_queryset = OrderInvoicingFile.objects.filter(invoicing=instance.id)
            if not invoicing_files_queryset.exists():
                errors.append('there is no attachment added')

            if (len(errors) > 0):
                raise serializers.ValidationError({'errors': errors})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class OrderInvoicingFilterSerializer(serializers.ModelSerializer):
    company_set = CompanySerializer(source='company',
                                    read_only=True)

    carrier_set = CarrierSerializer(source='carrier',
                                    read_only=True)

    client_set = ClientSerializer(source='client',
                                  read_only=True)

    status_set = OrderInvoicingStatusSerializer(source='status',
                                                read_only=True)


    class Meta:
        model = OrderInvoicingFilter
        fields = [
            'id',
            'name',
            'delivery_number',
            'commitment_number',
            'company',
            'company_set',
            'note_number',
            'carrier',
            'carrier_set',
            'client',
            'client_set',
            'status',
            'status_set',
            'nf_payed',
            'date_delivery_gte',
            'date_delivery_lte',
            'invoicing_delivery_date_gte',
            'invoicing_delivery_date_lte',
            'real_pay_date_gte',
            'real_pay_date_lte',
            'invoicing_date_gte',
            'invoicing_date_lte',
            'situation',
        ]
