from apps.permission.models import PermissionOptions
from apps.accounts.models import Profile
from apps.accounts.models import AccountProfile
from apps.accounts.models import PERMANENT_ACTIVE_MODULES
from apps.utils.cache import cache_method

@cache_method(timeout=60)
def validate_permission(uuid, app_option, has_permission):
    profile_qs = Profile.objects.filter(user__uuid=uuid)

    if (profile_qs.exists() == False):
        raise ValueError(f"Cannot find user uuid: {uuid}")

    profile = profile_qs.first()

    if (profile.user.is_superuser or
        profile.user.is_staff):
        return True

    if (profile.is_admin and
        profile.account != profile.context_account and
        profile.context_account.is_master == False):

        if (app_option in PERMANENT_ACTIVE_MODULES):
            return True
        else:
            account_profile_qs = AccountProfile.objects.filter(
                    id=profile.context_account.profile.id,
                    modules__contains=[{"key": app_option, "value": True}])
                                        
            return account_profile_qs.exists()

    if has_permission == 'permission_read':
        permission_qs = PermissionOptions.objects.filter(
                profile__user__user__uuid=uuid,
                app_option=app_option,
                permission_read=True)

    elif has_permission == 'permission_write':
        permission_qs = PermissionOptions.objects.filter(
                profile__user__user__uuid=uuid,
                app_option=app_option,
                permission_write=True)

    elif has_permission == 'permission_update':
        permission_qs = PermissionOptions.objects.filter(
                profile__user__user__uuid=uuid,
                app_option=app_option,
                permission_update=True)

    elif has_permission == 'permission_delete':
        permission_qs = PermissionOptions.objects.filter(
                profile__user__user__uuid=uuid,
                app_option=app_option,
                permission_delete=True)
    else:
        raise ValueError("Fail to validate permission")

    return permission_qs.exists()
