from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from django_multitenant.utils import get_current_tenant

User = get_user_model()

READ_METHOD = ['GET', 'HEAD', 'OPTIONS']
WRITE_METHOD = ['POST']
EDIT_METHOD = ['PUT', 'PATCH']
DELETE_METHOD = ['DELETE']
MODEL_NAME = 'User'


class IsAuthenticatedOrWriteOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in WRITE_METHOD or
            request.user and request.user.is_authenticated
        )
    
class IsProfileOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class HasModelPermission(BasePermission):

    def has_profile_permission(self, user, app_option, has_permission):
        user = User.objects.get(uuid=user.uuid)
        is_permission_true = False
        tenant = get_current_tenant()

        if (tenant.id == user.profile.account.id):
            if user.profile.permission is not None:
                permission = user.profile.permission.options.get(app_option=app_option)
                true_or_false = getattr(permission, has_permission)
                if true_or_false == True:
                    is_permission_true = true_or_false
            return is_permission_true
        else:
            return True

    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True

        if request.method in READ_METHOD:
            is_true = self.has_profile_permission(user=request.user,
                                                  app_option=MODEL_NAME,
                                                  has_permission="permission_read")
            return is_true

        if request.method in WRITE_METHOD:
            is_true = self.has_profile_permission(user=request.user,
                                                  app_option=MODEL_NAME,
                                                  has_permission="permission_write")
            return is_true

        if request.method in EDIT_METHOD:
            is_true = self.has_profile_permission(user=request.user,
                                                  app_option=MODEL_NAME,
                                                  has_permission="permission_update")
            return is_true

        if request.method in DELETE_METHOD:
            is_true = self.has_profile_permission(user=request.user,
                                                  app_option=MODEL_NAME,
                                                  has_permission="permission_delete")
            return is_true

        return False

class HasOtherPermission(BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(uuid=request.user.uuid)
        modules_permissions = user.profile.get_permissions_for_modules()

        if request.user.is_superuser:
            return True

        if request.method in READ_METHOD:
            is_true = modules_permissions['bidding']['can_read']
            is_true |= modules_permissions['bidding']['can_write']
            is_true |= modules_permissions['bidding']['can_edit']
            is_true |= modules_permissions['bidding']['can_delete']
            return is_true

        return False
