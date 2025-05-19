from django.db import transaction
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django_multitenant.utils import get_current_tenant
from django_multitenant.utils import set_current_tenant

from apps.permission.serializers import (
    ProfilePermissionBasicSerializer,
)

from .models import (
    User,
    Profile,
    Account,
    AccountProfile,
)

from apps.company.models import (
    CompanyCertificateStatus,
)

from apps.permission.models import (
    ProfilePermissions,
    PermissionOptions,
)

from apps.bidding.models import (
    Dispute,
    BiddingType,
    Modality,
    Interest,
    Phase,
    Status,
    Requirement,
)

from apps.order.models import (
    OrderInterest,
    OrderCommitmentStatus,
    OrderDeliveryStatus,
    OrderAssistanceStatus,
    OrderInvoicingStatus,
    OrderAssistanceType,
)

from apps.contract.models import (
    ContractScope,
    ContractType,
    ContractStatus,
)

from apps.supplier.models import (
    Category,
)

from apps.product.models import (
    Unity,
    Warranty,
    Classifier,
    Type,
)

from apps.address.serializers import (
    CountrySerializer,
    StateSerializer,
    CitySerializer,
    AddressTypeSerializer,
)

class AccountBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'name',
            'cnpj',
            'situation',
        ]

class ProfileSerializer(serializers.ModelSerializer):
    permission_set = ProfilePermissionBasicSerializer(source='permission', read_only=True)

    country_set = CountrySerializer(source='country', read_only=True)
    state_set = StateSerializer(source='state', read_only=True)
    city_set = CitySerializer(source='city', read_only=True)
    address_type_set = AddressTypeSerializer(source='address_type', read_only=True)

    context_account_set = AccountBasicSerializer(source='context_account', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'first_name',
            'last_name',
            'bio',
            'phone_number',
            'address',
            'address_type',
            'address_type_set',
            'number',
            'neighborhood',
            'complement',
            'city',
            'city_set',
            'state',
            'state_set',
            'country',
            'country_set',
            'zip_code',
            'get_full_name',
            'get_uuid',
            'get_email',
            'permission',
            'permission_set',
            'get_permissions_for_modules',
            'is_active',
            'commission',
            'account',
            'context_account',
            'context_account_set',
            'is_admin'
        ]
        read_only_fields = ('is_admin',)

class ProfileFormSerializer(serializers.ModelSerializer):
    permission_set = ProfilePermissionBasicSerializer(source='permission', read_only=True)

    country_set = CountrySerializer(source='country', read_only=True)
    state_set = StateSerializer(source='state', read_only=True)
    city_set = CitySerializer(source='city', read_only=True)
    address_type_set = AddressTypeSerializer(source='address_type', read_only=True)

    class Meta:
        model = Profile
        fields = ['id',
                  'first_name',
                  'last_name',
                  'bio',
                  'phone_number',
                  'address',
                  'address_type',
                  'address_type_set',
                  'number',
                  'neighborhood',
                  'complement',
                  'city',
                  'city_set',
                  'state',
                  'state_set',
                  'country',
                  'country_set',
                  'zip_code',
                  'get_uuid',
                  'get_email',
                  'permission',
                  'permission_set',
                  'get_permissions_for_modules',
                  'is_active',
                  'commission',
                  ]

class ProfileBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id',
                  'first_name',
                  'last_name',
                  'get_full_name',
                  'get_uuid',
                  'commission',
                  ]

class ProfileToOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id',
                  'get_full_name',
                  ]

class ProfileAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id',
                  'first_name',
                  'last_name',
                  'get_full_name',
                  'get_uuid',
                  'commission',
                  'is_active',
                  ]

class ProfileListSerializer(serializers.ModelSerializer):
    permission_set = ProfilePermissionBasicSerializer(source='permission', read_only=True)

    class Meta:
        model = Profile
        fields = ['id',
                  'first_name',
                  'last_name',
                  'get_full_name',
                  'get_uuid',
                  'permission',
                  'permission_set',
                  'is_active',
                  'commission',
                  ]

class ProfileAccountContextSerializer(serializers.ModelSerializer):
    select_account = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Profile
        fields = ['id',
                  'select_account'
        ]

    def update(self, instance, validated_data):
        account = validated_data.pop('select_account', None)

        account_qs = Account.objects.get_queryset_raw()
        new_context = account_qs.filter(id=account)

        if new_context.exists():
            instance.context_account = new_context.first()
            instance.save()

        return instance
class AccountNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'name',
            'is_master',
        ]

class ProfileAccountContextNameSerializer(serializers.ModelSerializer):
    context_account_set = AccountNameSerializer(source='context_account', read_only=True)
    class Meta:
        model = Profile
        fields = ['id',
                  'account',
                  'context_account',
                  'context_account_set',
        ]

class UserProfileListSerializer(serializers.ModelSerializer):
    profile = ProfileListSerializer()

    class Meta:
        model = User
        fields = [
            'uuid',
            'email',
            'is_active',
            'profile',
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileListSerializer()

    class Meta:
        model = User
        ordering = ['date_joined']
        fields = [
            'uuid',
            'email',
            'is_active',
            'profile',
            'password',
            'is_superuser',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        tenant = get_current_tenant()
        user = User.objects.create(
            email=validated_data['email'],
            account=tenant,
        )
        user.set_password(validated_data['password'])
        user.save()
        profile = user.profile
        profile_data = validated_data.pop('profile')
        profile.first_name = profile_data.get('first_name', profile.first_name)
        profile.last_name = profile_data.get('last_name', profile.last_name)
        profile.bio = profile_data.get('bio', profile.bio)
        profile.phone_number = profile_data.get(
            'phone_number', profile.phone_number
        )
        profile.address = profile_data.get('address', profile.address)
        profile.address_type = profile_data.get('address_type', profile.address)
        profile.number = profile_data.get('number', profile.number)
        profile.neighborhood = profile_data.get('neighborhood',
                                                profile.neighborhood)
        profile.complement = profile_data.get('complement', profile.complement)
        profile.city = profile_data.get('city', profile.city)
        profile.state = profile_data.get('state', profile.state)
        profile.country = profile_data.get('country', profile.country)
        profile.zip_code = profile_data.get('zip_code', profile.zip_code)
        profile.permission = profile_data.get('permission', profile.permission)
        profile.commission = profile_data.get('commission', profile.commission)
        profile.save()
        return user

    def update(self, instance, validated_data):
        profile = instance.profile
        profile_data = validated_data.pop('profile')
        profile.first_name = profile_data.get('first_name', profile.first_name)
        profile.last_name = profile_data.get('last_name', profile.last_name)
        profile.bio = profile_data.get('bio', profile.bio)
        profile.phone_number = profile_data.get('phone_number',
                                                profile.phone_number)
        profile.address = profile_data.get('address', profile.address)
        profile.address_type = profile_data.get('address_type', profile.address)
        profile.number = profile_data.get('number', profile.number)
        profile.neighborhood = profile_data.get('neighborhood',
                                                profile.neighborhood)
        profile.complement = profile_data.get('complement', profile.complement)
        profile.city = profile_data.get('city', profile.city)
        profile.state = profile_data.get('state', profile.state)
        profile.country = profile_data.get('country', profile.country)
        profile.zip_code = profile_data.get('zip_code', profile.zip_code)
        profile.permission = profile_data.get('permission', profile.permission)
        profile.commission = profile_data.get('commission', profile.commission)
        profile.save()
        return super(UserProfileSerializer, self).update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    new_password = serializers.CharField(required=True)
    
class UserImageSerializer(serializers.Serializer):
    model = Profile
    image = Base64ImageField(required=True, represent_in_base64=True)

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance

class ActiveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'is_active',
        ]

class AccountSelectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'name',
        ]

class AccountListSerializer(serializers.ModelSerializer):
    profile_set = serializers.SerializerMethodField()

    def get_profile_set(self, obj):
        serializer = AccountProfileSelectListSerializer(obj.profile)
        return serializer.data

    class Meta:
        model = Account
        fields = [
            'id',
            'name',
            'cnpj',
            'situation',
            'profile',
            'profile_set',
        ]

class AccountSerializer(serializers.ModelSerializer):
    country_set = CountrySerializer(source='country', read_only=True)

    state_set = StateSerializer(source='state', read_only=True)

    city_set = CitySerializer(source='city', read_only=True)

    profile_set = serializers.SerializerMethodField()

    def get_profile_set(self, obj):
        serializer = AccountProfileSelectListSerializer(obj.profile)
        return serializer.data

    class Meta:
        model = Account
        fields = [
            'id',
            'name',
            'cnpj',
            'owner_name',
            'owner_email',
            'owner_phone_number',
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
            'situation',
            'profile',
            'profile_set',
            'is_master',
        ]
        read_only_fields = ('is_master',)

    def copy_queryset(self, queryset, obj_model, account_destine):
        set_current_tenant(account_destine)

        for origin in queryset:
            filter = {}

            new_obj = {
                'account': account_destine
            }

            for field in origin._meta.get_fields():
                if not field.is_relation and field.name != 'id' and field.name != 'account' and field.name != 'pk':
                    filter[field.name] = getattr(origin, field.name)
                    new_obj[field.name] = getattr(origin, field.name)

            existing_obj = obj_model.objects.filter(account=account_destine, **filter).first()

            if not existing_obj:
                obj = obj_model(**new_obj)
                obj.save()

    def create_settings(self, account_origin, account_destine, setting_model):
        qs = setting_model.objects.get_queryset_raw()
        qs = qs.filter(account=account_origin)

        self.copy_queryset(qs, setting_model, account_destine)

    def create_fixed_settings(self, account_destine):
        master_account = Account.objects.get_queryset_raw().filter(is_master=True).first()

        self.create_settings(master_account, account_destine, CompanyCertificateStatus)
        self.create_settings(master_account, account_destine, OrderAssistanceType)
        self.create_settings(master_account, account_destine, ContractType)
        self.create_settings(master_account, account_destine, ContractScope)

    def setup_permission(self, account_origin, account_destine):
        set_current_tenant(account_origin)

        profile_qs = ProfilePermissions.objects.get_queryset_raw()

        for profile in profile_qs.filter(account=account_origin):
            set_current_tenant(account_destine)

            profile_obj = None
            options_qs = PermissionOptions.objects.get_queryset_raw()
            
            existing_profile = ProfilePermissions.objects.filter(
                name=profile.name,
                account=account_destine
            ).first()

            if existing_profile:
                profile_obj = existing_profile
            else:
                profile_obj = ProfilePermissions.objects.create(
                    name=profile.name,
                    description=profile.description,
                    audit_commitment=profile.audit_commitment,
                    audit_delivery=profile.audit_delivery,
                    account=account_destine,
                )

            for options in options_qs.filter(account=account_origin, profile=profile):
                set_current_tenant(account_destine)
                
                existing_options = PermissionOptions.objects.filter(
                    app_option=options.app_option,
                    profile=profile_obj,
                    account=account_destine
                ).first()

                if existing_options:
                    existing_options.permission_read = options.permission_read
                    existing_options.permission_write = options.permission_write
                    existing_options.permission_update = options.permission_update
                    existing_options.permission_delete = options.permission_delete
                    existing_options.save()
                else:
                    PermissionOptions.objects.create(
                        app_option=options.app_option,
                        permission_read=options.permission_read,
                        permission_write=options.permission_write,
                        permission_update=options.permission_update,
                        permission_delete=options.permission_delete,
                        profile=profile_obj,
                        account=account_destine,
                    )

                set_current_tenant(account_origin)

    def clone_bidding_phase_status(self, account_origin, account_destine):
        set_current_tenant(account_origin)

        phase_qs = Phase.objects.get_queryset_raw()
        phase_qs = phase_qs.filter(account=account_origin)

        for phase in phase_qs:
            set_current_tenant(account_destine)

            existing_phase = Phase.objects.filter(
                name=phase.name,
                account=account_destine
            ).first()

            if existing_phase:
                phase_obj = existing_phase
                phase_obj.color = phase.color
                phase_obj.save()
            else:
                phase_obj = Phase.objects.create(
                    name=phase.name,
                    color=phase.color,
                    account=account_destine,
                )

            set_current_tenant(account_origin)

            status_qs = Status.objects.get_queryset_raw()
            status_qs = status_qs.filter(phase=phase, account=account_origin)

            for status in status_qs:
                set_current_tenant(account_destine)

                existing_status = Status.objects.filter(
                    name=status.name,
                    phase=phase_obj,
                    account=account_destine
                ).first()

                if existing_status:
                    existing_status.color = status.color
                    existing_status.initial = status.initial
                    existing_status.save()
                else:
                    Status.objects.create(
                        name=status.name,
                        color=status.color,
                        phase=phase_obj,
                        initial=status.initial,
                        account=account_destine,
                    )

                set_current_tenant(account_origin)

    def setup_bidding(self, account_origin, account_destine):
        self.create_settings(account_origin, account_destine, Dispute)
        self.create_settings(account_origin, account_destine, BiddingType)
        self.create_settings(account_origin, account_destine, Modality)
        self.create_settings(account_origin, account_destine, Interest)
        self.create_settings(account_origin, account_destine, Requirement)

        self.clone_bidding_phase_status(account_origin, account_destine)

    def setup_order(self, account_origin, account_destine):
        self.create_settings(account_origin, account_destine, OrderInterest)
        self.create_settings(account_origin, account_destine, OrderCommitmentStatus)
        self.create_settings(account_origin, account_destine, OrderDeliveryStatus)
        self.create_settings(account_origin, account_destine, OrderAssistanceStatus)
        self.create_settings(account_origin, account_destine, OrderInvoicingStatus)

    def setup_contract(self, account_origin, account_destine):
        self.create_settings(account_origin, account_destine, ContractStatus)

    def setup_supplier(self, account_origin, account_destine):
        self.create_settings(account_origin, account_destine, Category)

    def setup_product(self, account_origin, account_destine):
        self.create_settings(account_origin, account_destine, Unity)
        self.create_settings(account_origin, account_destine, Warranty)
        self.create_settings(account_origin, account_destine, Classifier)
        self.create_settings(account_origin, account_destine, Type)

    def create(self, validated_data):
        try:
            account_qs = Account.objects.get_queryset_raw()
            account_qs = account_qs.order_by('-id')

            next_id = 1
            if account_qs.exists():
                next_id = int(account_qs.first().id) + 1

            validated_data['id'] = next_id

            with transaction.atomic():
                account = Account.objects.create(**validated_data)

                self.create_fixed_settings(account)

                for model_settings in account.profile.account_model_settings:
                    if model_settings['key'] == 'Permission':
                        self.setup_permission(account.profile.account_model, account)

                    if model_settings['key'] == 'BiddingSettings':
                        self.setup_bidding(account.profile.account_model, account)

                    if model_settings['key'] == 'OrderSettings':
                        self.setup_order(account.profile.account_model, account)

                    if model_settings['key'] == 'ContractSettings':
                        self.setup_contract(account.profile.account_model, account)
                        
                    if model_settings['key'] == 'SupplierSettings':
                        self.setup_supplier(account.profile.account_model, account)

                    if model_settings['key'] == 'ProductSettings':
                        self.setup_product(account.profile.account_model, account)

                return account
        except Exception as e:
            raise serializers.ValidationError("Fail to create account. Error: {exception}".format(exception=str(e)))
        
    def update(self, instance, validated_data):
        with transaction.atomic():            
            update_profile = validated_data.get('profile')

            if instance.profile != update_profile:
                for model_settings in update_profile.account_model_settings:
                    if model_settings['key'] == 'Permission':
                        self.setup_permission(update_profile.account_model, instance)

                    if model_settings['key'] == 'BiddingSettings':
                        self.setup_bidding(update_profile.account_model, instance)

                    if model_settings['key'] == 'OrderSettings':
                        self.setup_order(update_profile.account_model, instance)

                    if model_settings['key'] == 'ContractSettings':
                        self.setup_contract(update_profile.account_model, instance)
                        
                    if model_settings['key'] == 'SupplierSettings':
                        self.setup_supplier(update_profile.account_model, instance)

                    if model_settings['key'] == 'ProductSettings':
                        self.setup_product(update_profile.account_model, instance)

            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

        return instance

class ProfileIsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'is_admin',
        ]

class AccountProfileSelectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountProfile
        fields = [
            'id',
            'name',
        ]

class AccountProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountProfile
        fields = [
            'id',
            'name',
            'situation',
        ]

class AccountProfileSerializer(serializers.ModelSerializer):
    account_model_set = AccountSelectListSerializer(source='account_model', read_only=True)
    account_model_request = serializers.CharField(write_only=True)

    class Meta:
        model = AccountProfile
        fields = [
            'id',
            'name',
            'situation',
            'modules',
            'account_model_settings',
            'account_model_set',
            'account_model_request',
        ]


    def create(self, validated_data):
        try:
            with transaction.atomic():
                account_model_list_qs = Account.objects.get_queryset_raw()
                account_model_qs = account_model_list_qs.filter(id=validated_data['account_model_request'])

                account_model_obj = {}
                if account_model_qs.exists():
                    account_model_obj = account_model_qs.first()
                else:
                    raise serializers.ValidationError({ 'error': f"Fail to get account model" })
                
                account_profile = AccountProfile.objects.create(name=validated_data['name'],
                                                                situation=validated_data['situation'],
                                                                modules=validated_data['modules'],
                                                                account_model_settings=validated_data['account_model_settings'],
                                                                account_model=account_model_obj,)

                response_account_profile = AccountProfileSerializer(account_profile).data

                return response_account_profile
        except Exception as e:
            raise serializers.ValidationError("Fail to create account profile. Error: {exception}".format(exception=str(e)))
        
    
    def update(self, instance, validated_data):
        account_model_list_qs = Account.objects.get_queryset_raw()
        account_model_qs = account_model_list_qs.filter(id=validated_data['account_model_request'])
        if account_model_qs.exists():
            instance.account_model = account_model_qs.first()

        instance.name = validated_data['name']
        instance.situation = validated_data['situation']
        instance.modules = validated_data['modules']
        instance.account_model_settings = validated_data['account_model_settings']

        instance.save()

        return instance