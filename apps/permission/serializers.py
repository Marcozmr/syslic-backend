from rest_framework import serializers
from .models import ProfilePermissions, PermissionOptions


class AppOptionField(serializers.ChoiceField):
    
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return object

        choice = ''

        if obj in self._choices:
            choice = self._choices[obj]

        return choice
    
    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key

        self.fail('invalid_choice', input=data)


class PermissionOptionsSerializer(serializers.ModelSerializer):
    app_option = AppOptionField(choices=PermissionOptions.APPS_CHOICES)
    class Meta:
        model = PermissionOptions
        fields = [
            'app_option',
            'permission_read',
            'permission_write',
            'permission_update',
            'permission_delete'
        ]


class ProfilePermissionBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePermissions
        fields = [
            'id',
            'name',
        ]

class ProfilePermissionSerializer(serializers.ModelSerializer):
    options = PermissionOptionsSerializer(many=True)

    class Meta:
        model = ProfilePermissions
        fields = [
            'id',
            'name',
            'description',
            'options',
            'audit_commitment',
            'audit_delivery',
        ]

    def create(self, validated_data):
        permissions_options_data = validated_data.pop('options')
        profile = ProfilePermissions.objects.create(**validated_data)

        for permission_option_data in permissions_options_data:
            PermissionOptions.objects.create(profile=profile,
                                             **permission_option_data)
        return profile

    def update(self, instance, validated_data):
        permissions_options_data = validated_data.pop('options')

        instance.name = validated_data.get('name', instance.name)

        instance.description = validated_data.get('description',
                                                  instance.description)
        
        instance.audit_commitment = validated_data.get('audit_commitment',
                                                instance.audit_commitment)
        
        instance.audit_delivery = validated_data.get('audit_delivery',
                                                instance.audit_delivery)
        
        instance.save()

        for permission_option_data in permissions_options_data:
            option_queryset = PermissionOptions.objects.filter(
                profile=instance,
                app_option=permission_option_data.get('app_option'))

            if option_queryset.exists():
                option = PermissionOptions.objects.get(
                    profile=instance,
                    app_option=permission_option_data.get('app_option'))

                option.permission_read = permission_option_data.get(
                    'permission_read')
                option.permission_write = permission_option_data.get(
                    'permission_write')
                option.permission_update = permission_option_data.get(
                    'permission_update')
                option.permission_delete = permission_option_data.get(
                    'permission_delete')

                option.save()
            else:
                PermissionOptions.objects.create(profile=instance,
                                                 **permission_option_data)

        return instance

class ProfilePermissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePermissions
        fields = [
            'id',
            'name',
            'description',
        ]
    
class UserAddProfileSerializer(serializers.ModelSerializer):
    user_uuid = serializers.UUIDField(required=True)
    to_remove = serializers.BooleanField(required=True)
    
    class Meta:
        model = ProfilePermissions
        fields = ['id', 'name', 'user_uuid', 'to_remove',]
        read_only_fields = ('name',)
