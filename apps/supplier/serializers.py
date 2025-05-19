from rest_framework import serializers

from .models import (
    Supplier,
    Category,
)

from apps.address.serializers import (
    CountrySerializer,
    StateSerializer,
    CitySerializer,
    AddressTypeSerializer,
    NeighborhoodTypeSerializer,
)

from apps.accounts.serializers import (
    ProfileSerializer,
)

from apps.transport.serializers import (
    FreightSerializer,
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]

class SupplierSerializer(serializers.ModelSerializer):
    country_set = CountrySerializer(source='country',
                                    read_only=True)

    state_set = StateSerializer(source='state',
                                read_only=True)

    city_set = CitySerializer(source='city',
                              read_only=True)

    address_type_set = AddressTypeSerializer(source='address_type',
                                             read_only=True)

    neighborhood_type_set = NeighborhoodTypeSerializer(source='neighborhood_type',
                           read_only=True)

    responsible_set = ProfileSerializer(source='responsible',
                                        read_only=True)

    category_set = CategorySerializer(source='category',
                                      many=True,
                                      read_only=True)

    responsible_set = ProfileSerializer(source='responsible',
                                        read_only=True)
    
    region_freight_set = FreightSerializer(source='region_freight',
                                            read_only=True)

    class Meta:
        model = Supplier
        fields = [
            'id',
            'name',
            'name_fantasy',
            'cnpj',
            'ie',
            'im',
            'email',
            'phone_number',
            'address',
            'address_type',
            'address_type_set',
            'neighborhood',
            'neighborhood_type',
            'neighborhood_type_set',
            'complement',
            'number',
            'city',
            'city_set',
            'state',
            'state_set',
            'country',
            'country_set',
            'zip_code',
            'responsible',
            'responsible_set',
            'pix_key',
            'account_owner',
            'bank_name',
            'bank_agency',
            'bank_account',
            'category',
            'category_set',
            'region_freight',
            'region_freight_set',
        ]

class SupplierNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id',
            'name',
            'name_fantasy',
        ]

class SupplierBasicSerializer(serializers.ModelSerializer):
    region_freight_set = FreightSerializer(source='region_freight',
                                            read_only=True)

    class Meta:
        model = Supplier
        fields = [
            'id',
            'cnpj',
            'name',
            'name_fantasy',
            'region_freight',
            'region_freight_set',
        ]

class SupplierListSerializer(serializers.ModelSerializer):
    category_set = CategorySerializer(source='category',
                                      many=True,
                                      read_only=True)
    
    city_set = CitySerializer(source='city',
                              read_only=True)
    
    state_set = StateSerializer(source='state',
                                read_only=True)

    class Meta:
        model = Supplier
        fields = [
            'id',
            'cnpj',
            'name',
            'name_fantasy',
            'category',
            'category_set',
            'phone_number',
            'city',
            'city_set',
            'state',
            'state_set',
        ]

    def to_representation(self, instance):
        instance = Supplier.objects.select_related('city','state').prefetch_related('category').get(pk=instance.pk)

        return super().to_representation(instance)