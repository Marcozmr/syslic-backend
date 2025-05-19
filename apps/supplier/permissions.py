from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

from apps.permission.validate import validate_permission

READ_METHOD = ['GET', 'HEAD', 'OPTIONS']
WRITE_METHOD = ['POST']
EDIT_METHOD = ['PUT', 'PATCH']
DELETE_METHOD = ['DELETE']
MODEL_NAME = 'Supplier'
MODEL_NAME_2 = 'SupplierSettings'

class IsAuthenticatedOrWriteOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in WRITE_METHOD or
            request.user and request.user.is_authenticated
        )

class HasModelPermission(BasePermission):

    def has_profile_permission(self, user, app_option, has_permission):
        return validate_permission(user.uuid, app_option, has_permission)

    def has_permission(self, request, view):

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

class HasModelSettingsPermission(BasePermission):

    def has_profile_permission(self, user, app_option, has_permission):
        return validate_permission(user.uuid, app_option, has_permission)

    def has_permission(self, request, view):

        if request.method in READ_METHOD:
            is_true = self.has_profile_permission(user=request.user,
                                                  app_option=MODEL_NAME_2,
                                                  has_permission="permission_read")
            return is_true

        if request.method in WRITE_METHOD:
            is_true = self.has_profile_permission(user=request.user,
                                                  app_option=MODEL_NAME_2,
                                                  has_permission="permission_write")
            return is_true

        if request.method in EDIT_METHOD:
            is_true = self.has_profile_permission(user=request.user,
                                                  app_option=MODEL_NAME_2,
                                                  has_permission="permission_update")
            return is_true

        if request.method in DELETE_METHOD:
            is_true = self.has_profile_permission(user=request.user,
                                                  app_option=MODEL_NAME_2,
                                                  has_permission="permission_delete")
            return is_true

        return False

class HasOtherPermission(BasePermission):

    def has_permission(self, request, view):
        User = get_user_model()
        user = User.objects.get(uuid=request.user.uuid)
        modules_permissions = user.profile.get_permissions_for_modules()

        if request.user.is_superuser:
            return True

        if request.method in READ_METHOD:
            is_true = modules_permissions['supplier']['can_read']
            is_true |= modules_permissions['supplier']['can_write']
            is_true |= modules_permissions['supplier']['can_edit']
            is_true |= modules_permissions['supplier']['can_delete']

            is_true |= modules_permissions['product']['can_read']
            is_true |= modules_permissions['product']['can_write']
            is_true |= modules_permissions['product']['can_edit']
            is_true |= modules_permissions['product']['can_delete']
            return is_true

        return False

