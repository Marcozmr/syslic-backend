import logging

from django.db.models.signals import post_save
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django_multitenant.utils import set_current_tenant
from rest_framework.authtoken.models import Token

from apps.accounts.models import (
    Profile,
)
from .serializers import (
    AccountProfileSerializer,
)

class TokenManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.token_list = {}
            self.account_list = {}

            post_save.connect(self.watch_change_user_context, sender=Profile) 

    def get_account(self, key):
        token = Token.objects.get(key=key)
        return token.user.profile.context_account

    def watch_change_user_context(self, sender, instance, created, **kwargs):
        if instance:
            if instance.id in self.account_list:
                self.account_list.pop(instance.id)

class AccountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                token_key = auth_header.split()[1]

                manager = TokenManager()
                account = manager.get_account(token_key)

                account_serializer =  AccountProfileSerializer(account).data
                user_is_admin = Token.objects.get(key=token_key).user.profile.is_admin

                if (account_serializer['situation'] == 'inactive') and (user_is_admin == False):
                    return HttpResponse(f'Account Inactive', status=401)


                if account:
                    set_current_tenant(account)
                else:
                    return HttpResponseForbidden("Fail to set tenant.")

            except Exception as e:
                logging.error(f"Fail to set tenant. Error: {str(e)}")
                return HttpResponseForbidden(f"Fail to set tenant. Error: {str(e)}")

        return self.get_response(request)

