from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()

READ_METHOD = ['GET', 'HEAD', 'OPTIONS']
WRITE_METHOD = ['POST']
EDIT_METHOD = ['PUT', 'PATCH']
DELETE_METHOD = ['DELETE']

class HasModelPermission(BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(uuid=request.user.uuid)
        modules_permissions = user.profile.get_permissions_for_modules()

        is_true = False

        if request.user.is_superuser:
            is_true = True

        elif request.method in READ_METHOD:
            is_true |= modules_permissions['supplier']['can_read']
            is_true |= modules_permissions['client']['can_read']
            is_true |= modules_permissions['company']['can_read']

        elif request.method in WRITE_METHOD:
            is_true |= modules_permissions['supplier']['can_write']
            is_true |= modules_permissions['client']['can_write']
            is_true |= modules_permissions['company']['can_write']

        elif request.method in EDIT_METHOD:
            is_true |= modules_permissions['supplier']['can_edit']
            is_true |= modules_permissions['client']['can_edit']
            is_true |= modules_permissions['company']['can_edit']

        elif request.method in DELETE_METHOD:
            is_true |= modules_permissions['supplier']['can_delete']
            is_true |= modules_permissions['client']['can_delete']
            is_true |= modules_permissions['company']['can_delete']

        return is_true
