from django.db import models
from django.db.models.signals import post_save
from django.db.models import UniqueConstraint
from django.conf import settings
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from django_multitenant.models import TenantModel
from django_multitenant.fields import TenantForeignKey

from apps.accounts.models import (
    User,
    Account,
    AccountTenantManager,
)


class ProfilePermissions(TenantModel):
    name = models.CharField(max_length=50,
                            blank=False,
                            null=False)

    description = models.TextField(max_length=200,
                                   null=True,
                                   blank=True)

    audit_commitment = models.BooleanField(default=False)

    audit_delivery = models.BooleanField(default=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='ProfilePermissions')

    objects = AccountTenantManager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_profile_permission_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_profile_permission_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"


class PermissionOptions(TenantModel):
    APPS_CHOICES = (
        ("Default", "Padrão"),
        ("User", "Usuários"),
        ("Permission", "Permissões"),
        ("Company", "Empresas"),
        ("Client", "Clientes"),
        ("Bidding", "Licitações"),
        ("BiddingSettings", "Configurações de Licitações"),
        ("Supplier", "Fornecedores"),
        ("SupplierSettings", "Configurações de Fornecedores"),
        ("Product", "Produtos"),
        ("ProductSettings", "Configurações de Produtos"),
        ("Transport", "Transporte"),
        ("TransportSettings", "Configurações de Transporte"),
        ("Order", "Pedidos"),
        ("OrderSettings", "Configurações de Pedidos"),
        ("Contract", "Contratos"),
        ("ContractSettings", "Configurações de Contratos"),
        ("Commission", "Comissões"),
        ("Report", "Relatórios"),
    )

    app_option = models.CharField("Modulos",
                                  max_length=50,
                                  choices=APPS_CHOICES,
                                  null=False, blank=False,
                                  default="Default")

    permission_read = models.BooleanField(verbose_name="Visualizar",
                                          default=False)

    permission_write = models.BooleanField(verbose_name="Criar",
                                           default=False)

    permission_update = models.BooleanField(verbose_name="Atualizar",
                                            default=False)

    permission_delete = models.BooleanField(verbose_name="Apagar",
                                            default=False)

    profile = models.ForeignKey(ProfilePermissions,
                                on_delete=models.CASCADE,
                                related_name="options")

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='PermissionOptions')

    objects = AccountTenantManager()

    def __str__(self):
        return f'{self.app_option}'

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_permission_options_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

@receiver(post_save, sender=PermissionOptions)
def logout_user_with_from_permission(sender, instance, created, **kwargs):
    if created is False:
        user_list = User.objects.filter(profile__permission=instance.profile)
        Token.objects.filter(user__in=user_list).delete()

