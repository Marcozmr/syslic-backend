from django.db import models
from django.db.models import UniqueConstraint

from django_multitenant.models import TenantModel
from django_multitenant.fields import TenantForeignKey

from apps.accounts.models import (
    Profile,
    Account,
)

class MetaData(TenantModel):
    profile = models.ForeignKey(Profile,
                                    on_delete=models.CASCADE,
                                    blank=False,
                                    null=False)

    tag = models.CharField(max_length=1000,
                           blank=False,
                           null=False)

    meta = models.JSONField(default=list, null=False, blank=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='MetaData')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_metadata_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"
