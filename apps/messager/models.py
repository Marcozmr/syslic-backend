from django.db import models
from django.db.models import UniqueConstraint

from django_multitenant.models import TenantModel
from django_multitenant.fields import TenantForeignKey

from apps.accounts.models import (
    Profile,
    Account,
)

class Message(TenantModel):
    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Profile,
                               on_delete=models.PROTECT,
                               blank=False,
                               null=False,
                               related_name="messages")

    module = models.CharField(max_length=255,
                              blank=False,
                              null=False)

    thread = models.CharField(max_length=255,
                              blank=False,
                              null=False)

    message = models.CharField(max_length=5000,
                               blank=False,
                               null=False)

    mentions = models.ManyToManyField(Profile,
                                      related_name="mentions",
                                      blank=True)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='Message')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_message_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class MessageVisualization(TenantModel):
    viewer = models.ForeignKey(Profile, 
                               on_delete=models.PROTECT,
                               blank=False,
                               null=False)

    message = TenantForeignKey(Message, 
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name="viewers")

    date = models.DateTimeField(auto_now_add=True)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='MessageVisualization')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_message_visualization_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

