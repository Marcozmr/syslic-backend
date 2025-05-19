from rest_framework import serializers

from .models import (
    Contact,
)

from apps.address.serializers import (
    CountrySerializer,
    StateSerializer,
    CitySerializer,
    AddressTypeSerializer,
    NeighborhoodTypeSerializer,
)

class ContactSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Contact
        fields = [
            'id',
            'name',
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
            'position',
            'sector',
            'company',
            'client',
            'supplier',
            'carrier',
        ]
