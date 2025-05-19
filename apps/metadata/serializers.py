from rest_framework import serializers

from .models import (
    MetaData,
)

class MetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaData
        fields = ['id',
                  'profile',
                  'tag',
                  'meta']

    def create(self, validated_data):
        try:
            queryset = MetaData.objects.filter(profile=validated_data.get('profile'), tag=validated_data.get('tag'))

            if queryset.count() > 0:
                meta = queryset.first()
                meta.profile = validated_data.get('profile')
                meta.tag = validated_data.get('tag')
                meta.meta = validated_data.get('meta')
            else:
                meta = MetaData(**validated_data)

            meta.save()

        except Exception as e:
            raise serializers.ValidationError("Fail to create or update metadata: Error: {exception}".format(exception=str(e)))

        return meta
