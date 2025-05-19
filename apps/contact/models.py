from django.db import models
from django.db.models import UniqueConstraint
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

from apps.client.models import (
    Client,
)

from apps.company.models import (
    Company,
)

from apps.supplier.models import (
    Supplier,
)

from apps.transport.models import (
    Carrier,
)

from apps.accounts.models import (
    Account,
)

class Contact(TenantModel):
    name = models.CharField(max_length=200,
                            blank=False,
                            null=False)

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

    position = models.CharField(max_length=50,
                                blank=True,
                                null=True)

    sector = models.CharField(max_length=50,
                              blank=True,
                              null=True)

    company = TenantForeignKey(Company,
                                on_delete=models.PROTECT,
                                related_name="contacts",
                                blank=True,
                                null=True)

    client = TenantForeignKey(Client,
                               on_delete=models.PROTECT,
                               related_name="contacts",
                               blank=True,
                               null=True)

    supplier = TenantForeignKey(Supplier,
                                 on_delete=models.PROTECT,
                                 related_name="contacts",
                                 blank=True,
                                 null=True)

    carrier = TenantForeignKey(Carrier,
                               on_delete=models.PROTECT,
                               related_name="contacts",
                               blank=True,
                               null=True)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='Contact')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_contact_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

