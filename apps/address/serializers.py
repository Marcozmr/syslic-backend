from rest_framework import serializers
from .models import (
        Country,
        State,
        City,
        AddressType,
        NeighborhoodType,
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = [
                'id',
                'name',
                'code',
                'country',
        ]

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
                'id',
                'name',
                'code',
                'state',
        ]

class AddressTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressType
        fields = '__all__'

class NeighborhoodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeighborhoodType
        fields = '__all__'
