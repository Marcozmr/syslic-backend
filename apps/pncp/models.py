import uuid
from django.db import models
from django.db.models import UniqueConstraint
from apps.utils.phone_validator import phone_regex
from django_multitenant.models import TenantModel

from apps.address.models import (
        State,
)

from apps.accounts.models import (
    Account,
)

class HiringModalitie(models.Model):
    nome = models.CharField(max_length=100,
                            unique=True,
                            blank=False,
                            null=False)

    codigo = models.CharField(max_length=100,
                              unique=True,
                              blank=False,
                              null=False)

class Spheres(models.Model):
    nome = models.CharField(max_length=100,
                            unique=True,
                            blank=False,
                            null=False)

    codigo = models.CharField(max_length=100,
                              unique=True,
                              blank=False,
                              null=False)

class Powers(models.Model):
    nome = models.CharField(max_length=100,
                            unique=True,
                            blank=False,
                            null=False)

    codigo = models.CharField(max_length=100,
                              unique=True,
                              blank=False,
                              null=False)

class TypeCallingInstrument(models.Model):
    nome = models.CharField(max_length=100,
                            unique=True,
                            blank=False,
                            null=False)

    codigo = models.CharField(max_length=100,
                              unique=True,
                              blank=False,
                              null=False)
                              
class PncpFilter(TenantModel):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)
                            
    hiring_modalities = models.ForeignKey(HiringModalitie,
                                          on_delete=models.PROTECT,
                                          blank=True,
                                          null=True,
                                          related_name="pncp_filter")

    state = models.ForeignKey(State,
                              on_delete=models.PROTECT,
                              blank=True,
                              null=True,
                              related_name="pncp_filter")

    city = models.JSONField(default=dict, null=True, blank=True)

    spheres = models.ForeignKey(Spheres,
                                on_delete=models.PROTECT,
                                blank=True,
                                null=True,
                                related_name="pncp_filter")
    
    powers = models.ForeignKey(Powers,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True,
                               related_name="pncp_filter")

    type_calling_instrument = models.ForeignKey(TypeCallingInstrument,
                                                on_delete=models.PROTECT,
                                                blank=True,
                                                null=True,
                                                related_name="pncp_filter")
    
    organ = models.JSONField(default=dict, null=True, blank=True)
                              
    unit = models.JSONField(default=dict, null=True, blank=True)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='PncpFilter')
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_pncpfilter_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_pncpfilter_name_account'),
        ]
    
    class TenantMeta:
        tenant_field_name = "account_id"
