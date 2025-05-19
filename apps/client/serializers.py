from rest_framework import serializers
from .models import Client

from apps.address.serializers import (
    CountrySerializer,
    StateSerializer,
    CitySerializer,
    AddressTypeSerializer,
    NeighborhoodTypeSerializer,
)

from apps.transport.serializers import (
    FreightSerializer,
)
class ClientSerializer(serializers.ModelSerializer):
    country_set = CountrySerializer(source='country', read_only=True)
    state_set = StateSerializer(source='state', read_only=True)
    city_set = CitySerializer(source='city', read_only=True)
    address_type_set = AddressTypeSerializer(source='address_type', read_only=True)
    neighborhood_type_set = NeighborhoodTypeSerializer(source='neighborhood_type', read_only=True)
    region_freight_set = FreightSerializer(source='region_freight', read_only=True)

    class Meta:
        model = Client
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
                  'region_freight',
                  'region_freight_set']

class ClientNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id',
                  'name',
                  'name_fantasy'
                ]
        
class ClientListSerialier(serializers.ModelSerializer):
    state_set = StateSerializer(source='state', read_only=True)
    city_set = CitySerializer(source='city', read_only=True)
    region_freight_set = FreightSerializer(source='region_freight', read_only=True)

    class Meta:
        model = Client
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
            'region_freight',
            'region_freight_set',
        ]

    def to_representation(self, instance):
        instance = Client.objects.select_related('city', 'state', 'region_freight').get(pk=instance.pk)

        return super().to_representation(instance)

class ClientBasicSerializer(serializers.ModelSerializer):
    city_set = CitySerializer(source='city', read_only=True)
    state_set = StateSerializer(source='state', read_only=True)
    region_freight_set = FreightSerializer(source='region_freight', read_only=True)

    class Meta:
        model = Client
        fields = ['id',
                  'name',
                  'name_fantasy',
                  'city',
                  'city_set',
                  'state',
                  'state_set',
                  'region_freight',
                  'region_freight_set',
                ]

class ClientNameCNPJSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'name',
            'name_fantasy',
            'cnpj'
        ]

class ClientNamePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id',
                  'name',
                  'name_fantasy',
                  'phone_number',
                ]