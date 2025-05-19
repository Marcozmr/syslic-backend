from django.db import models
from django.db.models import UniqueConstraint

from django_cpf_cnpj.fields import CNPJField
from apps.utils.phone_validator import phone_regex

from django_multitenant.models import TenantModel
from django_multitenant.fields import TenantForeignKey

from apps.address.models import (
        Country,
        State,
        City,
        AddressType,
        NeighborhoodType,
)

from apps.transport.models import (
    Freight,
)

from apps.accounts.models import (
    Account,
)

class Client(TenantModel):
    name = models.CharField(max_length=100)

    name_fantasy = models.CharField(max_length=100,
                                    blank=True,
                                    null=True)

    cnpj = CNPJField(max_length=50,
                     blank=True,
                     null=True)

    ie = models.CharField(max_length=50,
                          blank=True,
                          null=True)

    im = models.CharField(max_length=50,
                          blank=True,
                          null=True)

    email = models.EmailField(blank=True,
                              null=True)


    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=17,
                                    blank=True,
                                    null=True)

    address_type = models.ForeignKey(AddressType,
                                     on_delete=models.PROTECT,
                                     blank=True,
                                     null=True)

    address = models.CharField(max_length=255,
                               blank=True,
                               null=True)

    neighborhood_type = models.ForeignKey(NeighborhoodType,
                                          on_delete=models.PROTECT,
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

    zip_code = models.CharField(max_length=50,
                                blank=True,
                                null=True)

    region_freight = TenantForeignKey(Freight,
                                       on_delete=models.PROTECT,
                                       blank=True,
                                       null=True)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='Client')

    class Meta:
        unique_together = (
            'id',
            'account',
        )
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_client_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_client_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

