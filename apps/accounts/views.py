from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import filters
from django.http import Http404
from django_filters import rest_framework as django_filters
from django_multitenant.utils import get_current_tenant
from django_multitenant.utils import set_current_tenant

from .models import (
    User,
    Profile,
    AccountProfile,
    Account,
)

from .serializers import (
    UserProfileSerializer,
    ProfileSerializer,
    ProfileAuthorSerializer,
    ProfileListSerializer,
    ProfileAccountContextSerializer,
    ProfileAccountContextNameSerializer,
    UserImageSerializer,
    ChangePasswordSerializer,
    ActiveUserSerializer,
    UserProfileListSerializer,
    AccountProfileListSerializer,
    AccountProfileSelectListSerializer,
    AccountProfileSerializer,
    AccountSelectListSerializer,
    AccountListSerializer,
    AccountSerializer,
    ProfileIsAdminSerializer,
)
from .permissions import (
    HasModelPermission,
    HasOtherPermission,
    IsProfileOwner,
)

from .pagination import AccountPagination

class UserProfileListViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = UserProfileListSerializer
    http_method_names = ['get', 'head']
    pagination_class = AccountPagination
    filter_backends = [filters.SearchFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'email',
        'profile__first_name',
        'profile__last_name',
        ]

    filter_fields = {
        'is_active': ['exact'],
        'profile__is_admin': ['exact'],
    }

    def get_queryset(self):
        queryset = User.objects.all().order_by('date_joined')
        tenant = get_current_tenant()
        return queryset.filter(account=tenant)

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

class UserProfileViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = UserProfileSerializer
    http_method_names = ['get', 'post', 'head']
    pagination_class = AccountPagination
    filter_backends = [filters.SearchFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'email',
        'profile__first_name',
        'profile__last_name',
        'profile__bio',
        'profile__phone_number',
        'profile__address',
        'profile__number',
        'profile__neighborhood',
        'profile__complement',
        'profile__zip_code',
        ]

    filter_fields = {
        'is_active': ['exact'],
        'profile__is_admin': ['exact'],
    }

    def get_queryset(self):
        queryset = User.objects.all().order_by('date_joined')
        tenant = get_current_tenant()
        return queryset.filter(account=tenant)

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

class ProfileDetail(GenericAPIView):
    permission_classes = (HasModelPermission | IsProfileOwner | HasOtherPermission,)
    serializer_class = ProfileSerializer
    fields = "__all__"

    def get_queryset(self):
        return Profile.objects.all()

    def get_object(self, id):
        try:
            return Profile.objects.get(user__uuid=id)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        profile = self.get_object(id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        profile = self.get_object(id)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        profile = self.get_object(id)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileDetailBasic(GenericAPIView):
    permission_classes = (HasModelPermission | IsProfileOwner | HasOtherPermission,)
    serializer_class = ProfileListSerializer
    fields = "__all__"

    def get_queryset(self):
        return Profile.objects.all()

    def get_object(self, id):
        try:
            return Profile.objects.get(user__uuid=id)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        profile = self.get_object(id)
        serializer = ProfileListSerializer(profile)
        return Response(serializer.data)

class ProfileAccountContextViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ProfileAccountContextSerializer
    http_method_names = ['put']

    def get_queryset(self):
        return Profile.objects.all().order_by('pk')

class ProfileAccountContextNameViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ProfileAccountContextNameSerializer
    http_method_names = ['get', 'options', 'head']

    def get_queryset(self):
        return Profile.objects.all().order_by('pk')

class ChangePasswordView(UpdateAPIView):
    permission_classes = (HasModelPermission | IsProfileOwner,)
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, id):
        try:
            tenant = get_current_tenant()
            return User.objects.get(uuid=id, account=tenant)
        except User.DoesNotExist:
            raise Http404

    def update(self, request, id, *args, **kwargs):
        tenant = get_current_tenant()
        user = User.objects.filter(uuid=id, account=tenant)

        if user.exists():
            self.object = self.get_object(id)
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                }
                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Cannot find user", status=status.HTTP_400_BAD_REQUEST)

class UserImageView(GenericAPIView):
    permission_classes = (HasModelPermission | IsProfileOwner | HasOtherPermission,)
    serializer_class = UserImageSerializer
    fields = "image"

    def get_queryset(self):
        return Profile.objects.all()

    def get_object(self, id):
        try:
            return Profile.objects.get(user__uuid=id)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        profile = self.get_object(id)
        serializer = UserImageSerializer(profile)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        profile = self.get_object(id)
        serializer = UserImageSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'User image updated successfully',
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        profile = self.get_object(id)
        profile.image.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ActivateUserView(UpdateAPIView):
    permission_classes = [HasModelPermission]
    serializer_class = UserProfileSerializer
    model = User

    def get_queryset(self):
        queryset = User.objects.all()
        tenant = get_current_tenant()
        return queryset.filter(account=tenant)

    def update(self, request, id, *args, **kwargs):
        tenant = get_current_tenant()
        user = User.objects.filter(uuid=id, account=tenant)

        if user.exists():
            serializer = ActiveUserSerializer(data=request.data)
            if(serializer.is_valid()):
                user = User.objects.get(uuid=id)
                user.is_active = serializer.data.get('is_active')
                user.save()

                response = ActiveUserSerializer(user)
                return Response(response.data)
            else:
                return Response(data='Fail to active/deactive user, the resquest is invalid', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data='Cannot find user', status=status.HTTP_400_BAD_REQUEST)

class ProfileAuthorViewSet(ModelViewSet):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | IsProfileOwner | HasOtherPermission,)
    serializer_class = ProfileAuthorSerializer
    pagination_class = AccountPagination

    def get_queryset(self):
        tenant = get_current_tenant()
        return Profile.objects.filter(account=tenant).order_by('pk')


class AccountProfileListViewSet(ModelViewSet):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = AccountProfileListSerializer
    pagination_class = AccountPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'id',
        'name',
        'situation',
    ]

    ordering_fields = [
        'id',
        'name',
        'situation',
    ]

    filter_fields = {
        'name': ['exact'],
        'situation': ['exact'],
    }

    def get_queryset(self):
        return AccountProfile.objects.all().order_by('pk')

class AccountProfileSelectListViewSet(ModelViewSet):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = AccountProfileSelectListSerializer
    pagination_class = AccountPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'id',
        'name',
    ]

    ordering_fields = [
        'id',
        'name',
    ]

    filter_fields = {
        'name': ['exact'],
    }

    def get_queryset(self):
        return AccountProfile.objects.all().order_by('pk')

class AccountProfileViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = AccountProfileSerializer
    pagination_class = AccountPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'id',
        'name',
        'situation',
        'account_model__name',
    ]

    ordering_fields = [
        'id',
        'name',
        'situation',
        'account_model__name',
    ]

    filter_fields = {
        'name': ['exact'],
        'situation': ['exact'],
        'account_model': ['exact'],
    }

    def get_queryset(self):
        return AccountProfile.objects.select_related('account_model').order_by('pk')

class AccountSelectListViewSet(ModelViewSet):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = AccountSelectListSerializer
    pagination_class = AccountPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'id',
        'name',
    ]

    ordering_fields = [
        'id',
        'name',
    ]

    filter_fields = {
        'name': ['exact'],
    }

    def get_queryset(self):
        account_qs = Account.objects.get_queryset_raw()
        return account_qs.all().order_by('pk')



class AccountListViewSet(ModelViewSet):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = AccountListSerializer
    pagination_class = AccountPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
        'id',
        'name',
        'cnpj',
        'situation',
        'profile__name',
    ]

    ordering_fields = [
        'id',
        'name',
        'cnpj',
        'situation',
        'profile__name',
    ]

    filter_fields = {
        'name': ['exact'],
        'cnpj': ['exact'],
        'situation': ['exact'],
        'profile': ['exact'],
        'is_master': ['exact'],
    }

    def get_queryset(self):
        account_qs = Account.objects.get_queryset_raw()
        return account_qs.select_related('profile').order_by('pk')

class AccountViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = AccountSerializer
    pagination_class = AccountPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]

    search_fields = [
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
        'state',
        'country',
        'zip_code',
        'situation',
        'profile__name',
    ]

    ordering_fields = [
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
        'state',
        'country',
        'zip_code',
        'situation',
        'profile__name',
    ]

    filter_fields = {
        'name': ['exact'],
        'cnpj': ['exact'],
        'owner_name': ['exact'],
        'owner_email': ['exact'],
        'owner_phone_number': ['exact'],
        'situation': ['exact'],
        'profile': ['exact'],
    }

    def get_queryset(self):
        account_qs = Account.objects.get_queryset_raw()
        return account_qs.select_related('profile').order_by('pk')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        set_current_tenant(instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileIsAdminViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ProfileIsAdminSerializer
    http_method_names = ['put']

    def get_queryset(self):
        return Profile.objects.all().order_by('pk')
