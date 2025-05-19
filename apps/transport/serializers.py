from rest_framework import serializers

from .models import (
    Freight,
    Carrier,
)

from apps.address.serializers import (
    CountrySerializer,
    StateSerializer,
    CitySerializer,
    AddressTypeSerializer,
    NeighborhoodTypeSerializer,
)

class FreightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freight
        fields = ['id',
                  'name',
                  'value']

class CarrierSerializer(serializers.ModelSerializer):
    country_set = CountrySerializer(source='country', read_only=True)
    state_set = StateSerializer(source='state', read_only=True)
    city_set = CitySerializer(source='city', read_only=True)
    address_type_set = AddressTypeSerializer(source='address_type', read_only=True)
    neighborhood_type_set = NeighborhoodTypeSerializer(source='neighborhood_type', read_only=True)

    class Meta:
        model = Carrier
        fields = ['id',
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
                  'pix_key',
                  'account_owner',
                  'bank_name',
                  'bank_agency',
                  'bank_account']

class CarrierListSerialier(serializers.ModelSerializer):
    state_set = StateSerializer(source='state', read_only=True)
    city_set = CitySerializer(source='city', read_only=True)

    class Meta:
        model = Carrier
        fields = [
            'id',
            'name',
            'name_fantasy',
            'ie',
            'cnpj',
            'email',
            'phone_number',
            'city',
            'city_set',
            'state',
            'state_set',
        ]

    def to_representation(self, instance):
        instance = Carrier.objects.select_related('city', 'state').get(pk=instance.pk)

        return super().to_representation(instance)

class CarrierNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = [
            'id',
            'name',
            'name_fantasy',
        ]

class CarrierToDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = [
            'id',
            'name',
            'name_fantasy',
            'email',
            'phone_number',
        ]
