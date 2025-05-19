from django.urls import include, path
from rest_framework import routers
from .views import (
    ProfilePermissionViewSet,
    ProfilePermissionListViewSet,
    UserAddOrRemoveProfileView,
)

app_name = 'permission'

router = routers.DefaultRouter()
router.register(r'permission-list', ProfilePermissionListViewSet, basename="ProfilePermissionList")
router.register(r'', ProfilePermissionViewSet, basename="profile-permission")


urlpatterns = [
    path('', include(router.urls)),
    path('user-add-or-remove-profile/<int:id>/', UserAddOrRemoveProfileView.as_view()),
]
