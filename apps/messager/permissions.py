from rest_framework.permissions import BasePermission

class HasModelPermission(BasePermission):

    def has_permission(self, request, view):
        return True
