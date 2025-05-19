from rest_framework import serializers
from django.db.models import Subquery
from apps.utils.fields import FileBase64Field

from .models import (
    HiringModalitie,
    Spheres,
    Powers,
    TypeCallingInstrument,
    PncpFilter,
)

from apps.address.serializers import (
    StateSerializer,
)

class HiringModalitieSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiringModalitie
        fields = [
            'id',
            'nome',
            'codigo',
        ]

class SpheresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spheres
        fields = [
            'id',
            'nome',
            'codigo',
        ]

class PowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Powers
        fields = [
            'id',
            'nome',
            'codigo',
        ]

class TypeCallingInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCallingInstrument
        fields = [
            'id',
            'nome',
            'codigo',
        ]

class PncpFilterSerializer(serializers.ModelSerializer):
    hiring_modalities_set = HiringModalitieSerializer(source='hiring_modalities',
                                                      read_only=True)

    state_set = StateSerializer(source='state',
                                read_only=True)

    spheres_set = SpheresSerializer(source='spheres',
                                    read_only=True)

    powers_set = PowersSerializer(source='powers',
                                  read_only=True)

    type_calling_instrument_set = TypeCallingInstrumentSerializer(source='type_calling_instrument',
                                                                  read_only=True)

    class Meta:
        model = PncpFilter
        fields = [
            'id',
            'name',
            'hiring_modalities',
            'hiring_modalities_set',
            'state',
            'state_set',
            'spheres',
            'spheres_set',
            'powers',
            'powers_set',
            'type_calling_instrument',
            'type_calling_instrument_set',
            'city',
            'organ',
            'unit',
        ]