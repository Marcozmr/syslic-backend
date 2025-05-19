from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import (
    User,
    Profile,
    Account,
    AccountProfile,
    Profile,
)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    

class UserAdmin(UserAdmin):
    list_display = [
        'email', 'is_active', 'is_staff', 'is_superuser'
    ]
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['email']
    filter_horizontal = ['user_permissions']

    fieldsets = [['Informações pessoais', {'fields': ['email']}]]
    add_fieldsets = [
        ['Informações pessoais', {
            'fields': ['email', 'password1', 'password2']
        }]
    ]

    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, UserAdmin)
admin.site.register(AccountProfile)
admin.site.register(Account)
admin.site.register(Profile)
