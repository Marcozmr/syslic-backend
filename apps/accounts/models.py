import uuid

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.deletion import CASCADE
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .managers import UserManager
from apps.utils.phone_validator import phone_regex
from django_cpf_cnpj.fields import CNPJField

from django_multitenant.models import TenantModel
from django_multitenant.mixins import TenantManagerMixin
from django_multitenant.utils import get_current_tenant

from apps.address.models import (
    Country,
    State,
    City,
    AddressType,
)

PERMANENT_ACTIVE_MODULES = [
    'User',
    'Permission',
    'Company',
    'Client',
    'Supplier',
    'SupplierSettings',
    'Product',
    'ProductSettings',
    'Transport',
    'TransportSettings',
]

class AccountProfile(models.Model):
    name = models.TextField(blank=False,
                            null=False)

    AccountProfileSituationChoices = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    situation = models.CharField(choices=AccountProfileSituationChoices,
                                 max_length=20,
                                 default='active')

    modules = models.JSONField(blank=True,
                               null=True)

    account_model_settings = models.JSONField(blank=True,
                                              null=True,)

    account_model = models.ForeignKey("Account",
                                      on_delete=models.PROTECT,
                                      blank=True,
                                      null=True)

class AccountTenantManager(TenantManagerMixin, models.Manager):
    use_in_migrations = True

    def get_queryset_raw(self):
        queryset = self._queryset_class(self.model)
        return queryset

class Account(TenantModel):
    objects = AccountTenantManager()

    name = models.TextField(blank=False,
                            null=False)

    cnpj = CNPJField(max_length=50,
                     blank=True,
                     null=True)

    owner_name = models.TextField(blank=True,
                                  null=True)


    owner_email = models.EmailField(blank=True,
                                    null=True)


    owner_phone_number = models.CharField(validators=[phone_regex],
                                    max_length=17,
                                    blank=True,
                                    null=True)

    address = models.CharField(max_length=255,
                               blank=True,
                               null=True)

    neighborhood = models.CharField(max_length=50,
                                    blank=True,
                                    null=True)

    number = models.CharField(max_length=50,
                                  blank=True,
                                  null=True)

    complement = models.CharField(max_length=1050,
                                  blank=True,
                                  null=True)

    city = models.ForeignKey(City,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)

    state = models.ForeignKey(State,
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True)

    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)

    zip_code = models.CharField(max_length=50,
                                blank=True,
                                null=True)

    AccountSituationChoices = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    situation = models.CharField(choices=AccountSituationChoices,
                                 max_length=20,
                                 default='active')

    profile = models.ForeignKey(AccountProfile,
                                on_delete=models.PROTECT,
                                blank=True,
                                null=True)

    is_master = models.BooleanField(default=False,
                                    blank=False,
                                    null=False)
    class Meta:
        unique_together = ["name", "cnpj"]

    class TenantMeta:
        tenant_field_name = "id"

class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=None, editable=False)

    username = models.CharField(
        _("username"), max_length=150, editable=False, blank=True
    )

    email = models.EmailField(_("email address"), unique=True)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='User')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not hasattr(self, 'account'):
            account_qs = Account.objects.get_queryset_raw()
            self.account = account_qs.filter(is_master=True).first()
        if self.pk is None:
            self.pk = uuid.uuid4()
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['uuid']),
            models.Index(fields=['email']),
        ]

class Profile(models.Model):
    def validate_image_size(field_file):
        file_size = field_file.file.size
        megabyte_limit = 5.0
        if file_size > megabyte_limit*1024*1024:
            raise ValidationError('Max file size is 5MB')

    def upload_to_path(self, filename):
        ext = filename.split('.')[-1]
        name = uuid.uuid4().hex
        return 'profile/{}.{}'.format(name, ext)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='Profile')

    context_account = models.ForeignKey(Account,
                                        on_delete=models.CASCADE,
                                        blank=False,
                                        null=False,
                                        related_name='context_account')

    image = models.ImageField(upload_to=upload_to_path,
                              blank=True,
                              null=True,
                              validators=[validate_image_size])

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='profile')

    first_name = models.CharField(verbose_name="first_name",
                                  max_length=255, blank=False)

    last_name = models.CharField(verbose_name="last_name",
                                 max_length=255, blank=False)

    bio = models.TextField(max_length=500,
                           blank=True)

    phone_number = models.CharField(verbose_name="phone",
                                    validators=[phone_regex],
                                    max_length=17, blank=False, null=False)

    address_type = models.ForeignKey(AddressType,
                                     on_delete=models.PROTECT,
                                     blank=True,
                                     null=True)

    address = models.CharField(
        verbose_name="address", max_length=255, blank=True, null=True)

    number = models.CharField(verbose_name="number",
                              max_length=50, blank=True, null=True)

    neighborhood = models.CharField(verbose_name="neighborhood",
                                    max_length=50, blank=True, null=True)

    complement = models.CharField(verbose_name="complement", 
                                  max_length=1050, blank=True, null=True)

    city = models.ForeignKey(City,
                             on_delete=models.PROTECT,
                             blank=True,
                             null=True)

    state = models.ForeignKey(State,
                              on_delete=models.PROTECT,
                              blank=True,
                              null=True)

    country = models.ForeignKey(Country,
                                on_delete=models.PROTECT,
                                blank=True,
                                null=True)

    zip_code = models.CharField(verbose_name="CEP",
                                max_length=50,
                                blank=True,
                                null=True)

    permission = models.ForeignKey('permission.ProfilePermissions',
                                  on_delete=models.PROTECT,
                                  related_name='user',
                                  blank=True,
                                  null=True)

    commission = models.DecimalField(decimal_places=2,
                                     max_digits=20,
                                     default=0.00,
                                     null=True,
                                     blank=True)

    admin_permission = models.JSONField(blank=True,
                                        null=True,)

    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.email}'

    def is_active(self):
        return f'{self.user.is_active}'

    def get_uuid(self):
        return f'{self.user.uuid}'

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name

    def get_email(self):
        return f'{self.user.email}'

    def get_permission_for_app(self, app, action):
        is_permission_true = False

        if (self.user.is_superuser or
            self.user.is_staff):
            is_permission_true = True

        elif (self.is_admin and
            self.account.id == self.context_account.id and
            self.context_account.is_master == True and
            app == "Admin"):
            is_permission_true = True

        elif (self.is_admin and
            self.account != self.context_account and
            self.context_account.is_master == False):

            if (app in PERMANENT_ACTIVE_MODULES):
                is_permission_true = True
            else:
                account_profile_qs = AccountProfile.objects.filter(
                        id=self.context_account.profile.id,
                        modules__contains=[{"key": app, "value": True}])

                is_permission_true = account_profile_qs.exists() 

        elif (self.is_admin and
            self.account == self.context_account and
            self.context_account.is_master == True):

            permission = self.permission.options.filter(
                app_option=app
            )

            if permission.exists():
                true_or_false = getattr(permission.first(), action)
                if true_or_false == True:
                    is_permission_true = true_or_false
            else:
                is_permission_true = False

        else:
            try:
                module_enabled = False

                if (app in PERMANENT_ACTIVE_MODULES or self.context_account.is_master):
                    module_enabled = True

                else:
                    account_profile_qs = AccountProfile.objects.filter(
                            id=self.context_account.profile.id,
                            modules__contains=[{"key": app, "value": True}])

                    module_enabled = account_profile_qs.exists()

                if (module_enabled and self.permission is not None):
                    permission = self.permission.options.filter(
                        app_option=app
                    )

                    if permission.exists():
                        true_or_false = getattr(permission.first(), action)
                        if true_or_false == True:
                            is_permission_true = true_or_false
                    else:
                        is_permission_true = False

            except ObjectDoesNotExist:
                is_permission_true = False

        return is_permission_true

    def get_permissions_for_modules(self):

        MODULES = (
            ('user', 'User'),
            ('permission', 'Permission'),
            ('company', 'Company'),
            ('client', 'Client'),
            ('bidding', 'Bidding'),
            ('bidding_settings', 'BiddingSettings'),
            ('supplier', 'Supplier'),
            ('supplier_settings', 'SupplierSettings'),
            ('product', 'Product'),
            ('product_settings', 'ProductSettings'),
            ('transport', 'Transport'),
            ('transport_settings', 'TransportSettings'),
            ('order_settings', 'OrderSettings'),
            ('order', 'Order'),
            ('contract', 'Contract'),
            ('contract_settings', 'ContractSettings'),
            ('commission', 'Commission'),
            ('report', 'Report'),

            # These module isnot avaialable for permission selection
            ('admin', 'Admin'),
        )

        PERMISSIONS = (
            ('can_read', 'permission_read'),
            ('can_edit', 'permission_update'),
            ('can_write', 'permission_write'),
            ('can_delete', 'permission_delete'),
        )

        permissions_modules = {}
        for key, value in MODULES:
            permissions_modules[key] = {}
            for action, permission in PERMISSIONS:
                permissions_modules[key][action] = self.get_permission_for_app(value, permission)

        ACTION = 'can_audit'
        AUDIT_MODULE = 'audit'
        AUDIT_MODULES_FIELD = (
            ('delivery', 'audit_delivery'),
            ('commitment', 'audit_commitment'),
        )

        permissions_modules[AUDIT_MODULE] = {}

        for key, value in AUDIT_MODULES_FIELD:
            permissions_modules[AUDIT_MODULE][key] = {}
            permissions_modules[AUDIT_MODULE][key][ACTION] = getattr(self.permission, value, False)

        return permissions_modules

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        tenant = get_current_tenant()
        if tenant is None:
            account_qs = Account.objects.get_queryset_raw()
            tenant = account_qs.filter(id=1).first()

        Profile.objects.create(user=instance,
                               account=tenant,
                               context_account=tenant)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()
