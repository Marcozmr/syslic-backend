from django.db.models import fields
from django.http.response import Http404
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from apps.accounts.models import User
from .models import ProfilePermissions
from .serializers import ProfilePermissionSerializer, ProfilePermissionListSerializer, UserAddProfileSerializer
from .permissions import HasModelPermission
from .pagination import PermissionPagination



class ProfilePermissionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission,)
    serializer_class = ProfilePermissionSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    pagination_class = PermissionPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
            'name',
            'description'
            ]

    def get_queryset(self):
        return ProfilePermissions.objects.all().order_by('pk')

class ProfilePermissionListViewSet(ModelViewSet):
    http_method_names = ['get', 'head']
    permission_classes = (HasModelPermission,)
    serializer_class = ProfilePermissionListSerializer
    pagination_class = PermissionPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
            'name',
            'description'
            ]

    def get_queryset(self):
        return ProfilePermissions.objects.all().order_by('pk')

class UserAddOrRemoveProfileView(UpdateAPIView):
    permission_classes =  (HasModelPermission,)
    serializer_class = UserAddProfileSerializer
    model = ProfilePermissions

    def get_queryset(self):
        return ProfilePermissions.objects.all()

    def get_object(self, id):
        try:
            return ProfilePermissions.objects.get(id=id)
        except ProfilePermissions.DoesNotExist:
            raise Http404

    def update(self, request, id, *args, **kwargs):
        self.object = self.get_object(id)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user_uuid = serializer.data.get("user_uuid")
            to_remove = serializer.data.get("to_remove")
            try:
                user = User.objects.get(uuid=user_uuid)
            except User.DoesNotExist:
                raise Http404
            if to_remove == False:
                self.object.members.add(user)
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': f'User add to {self.object.name} successfully',
                }
                return Response(response)
            else:
                self.object.members.remove(user)
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': f'User removed from {self.object.name} successfully',
                }
                return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


