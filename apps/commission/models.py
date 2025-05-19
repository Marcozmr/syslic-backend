from django.db import models
from django.db.models import UniqueConstraint

from django_multitenant.models import TenantModel
from django_multitenant.fields import TenantForeignKey

from apps.order.models import (
    OrderInvoicing,
)

from apps.accounts.models import (
    Profile,
    Account,
)

class Commission(TenantModel):
    owner = models.ForeignKey(Profile,
                              related_name='commission_owner',
                              on_delete=models.PROTECT,
                              blank=False,
                              null=False)

    invoicing = TenantForeignKey(OrderInvoicing,
                                 related_name='commission_invoicing',
                                 on_delete=models.PROTECT,
                                 blank=False,
                                 null=False)
    
    commission_percentage = models.DecimalField(decimal_places=2,
                                                max_digits=20,
                                                default=0.01,
                                                null=False,
                                                blank=False)

    notes = models.TextField(null=True,
                             blank=True)

    StatusChoices = (
        ('pending', 'Pending'),
        ('released', 'Released'),
        ('payed', 'Payed'),
    )

    status = models.CharField(choices=StatusChoices,
                              default='pending',
                              max_length=100)
            
    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='Commission')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_commission_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

