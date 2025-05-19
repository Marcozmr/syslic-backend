from django.urls import include, path
from rest_framework import routers
from .views import (
    UserProfileViewSet,
    UserProfileListViewSet,
    ProfileDetail,
    ProfileDetailBasic,
    ProfileAccountContextViewSet,
    ProfileAccountContextNameViewSet,
    UserImageView,
    ChangePasswordView,
    ActivateUserView,
    ProfileAuthorViewSet,
    AccountProfileListViewSet,
    AccountProfileViewSet,
    AccountProfileSelectListViewSet,
    AccountSelectListViewSet,
    AccountListViewSet,
    AccountViewSet,
    ProfileIsAdminViewSet,
)

app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'user', UserProfileViewSet, basename="Profile")
router.register(r'user-list', UserProfileListViewSet, basename="ProfileList")
router.register(r'author', ProfileAuthorViewSet, basename="ProfileAuthor")
router.register(r'account', AccountViewSet, basename="Account")
router.register(r'profile-is-admin', ProfileIsAdminViewSet, basename="ProfileIsAdmin")
router.register(r'account-select', AccountSelectListViewSet, basename="AccountSelectList")
router.register(r'account-list', AccountListViewSet, basename="AccountList")
router.register(r'account-profile', AccountProfileViewSet, basename="AccountProfile")
router.register(r'account-profile-select', AccountProfileSelectListViewSet, basename="AccountProfileSelectList")
router.register(r'account-profile-list', AccountProfileListViewSet, basename="AccountProfileList")
router.register(r'user/account/context', ProfileAccountContextViewSet, basename="ProfileAccountContext")
router.register(r'user/account/context-name', ProfileAccountContextNameViewSet, basename="ProfileAccountContextName")

urlpatterns = [
    path('', include(router.urls)),
    path('user/activate/<uuid:id>/', ActivateUserView.as_view()),
    path('user-profile/<uuid:id>/', ProfileDetail.as_view()),
    path('user-profile-basic/<uuid:id>/', ProfileDetailBasic.as_view()),
    path('user-change-password/<uuid:id>/', ChangePasswordView.as_view()),
    path('user/photo/<uuid:id>/', UserImageView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
