import uuid
from django.db import models
from django.db.models import UniqueConstraint
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError

from django_multitenant.models import TenantModel
from django_multitenant.fields import TenantForeignKey

from apps.bidding.models import (
    Bidding,
    BiddingItem,
    BiddingItemCompound,
)

from apps.client.models import (
    Client,
)

from apps.company.models import (
    Company,
)

from apps.product.models import (
    Product,
)

from apps.accounts.models import (
    Profile,
    Account,
    AccountTenantManager,
)

class ContractType(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='ContractType')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_contract_type_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_contract_type_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class ContractScope(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='ContractScope')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_contract_scope_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_contract_scope_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class ContractStatus(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    color = models.CharField(max_length=100,
                             blank=False,
                             null=False)

    initial = models.BooleanField(default=False)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='contract_status')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_contract_status_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_contract_status_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class ContractFilter(TenantModel):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    client = TenantForeignKey(Client,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True,
                               related_name="contract_filter")

    company = TenantForeignKey(Company,
                                on_delete=models.PROTECT,
                                blank=True,
                                null=True,
                                related_name="contract_filter")

    status = TenantForeignKey(ContractStatus,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True,
                               related_name="contract_filter")

    type = TenantForeignKey(ContractType,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True,
                               related_name="contract_filter")

    scope = TenantForeignKey(ContractScope,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True,
                               related_name="contract_filter")

    state = models.CharField(max_length=10,
                             blank=True,
                             null=True)

    date_start = models.DateField(null=True,
                                  blank=True)

    date_finish = models.DateField(null=True,
                                   blank=True)

    number = models.CharField(max_length=100,
                              blank=True,
                              null=True)

    is_outdated = models.BooleanField(null=True)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='ContractFilter')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_contract_filter_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_contract_filter_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class Contract(TenantModel):
    bidding = TenantForeignKey(Bidding,
                                related_name='contract',
                                on_delete=models.PROTECT,
                                blank=False,
                                null=False)

    status = TenantForeignKey(ContractStatus,
                               on_delete=models.PROTECT,
                               blank=False,
                               null=False)

    scope = TenantForeignKey(ContractScope,
                              on_delete=models.PROTECT,
                              blank=False,
                              null=False)

    type = TenantForeignKey(ContractType,
                             on_delete=models.PROTECT,
                             blank=False,
                             null=False)

    date_start = models.DateField(null=True, blank=True)

    date_finish = models.DateField(null=True, blank=True)

    number = models.CharField(max_length=100,
                               blank=False,
                               null=False)

    observation = models.TextField(null=True,
                                   blank=True)

    owner = models.ForeignKey(Profile,
                              on_delete=models.PROTECT,
                              blank=True,
                              null=True)

    StateChoices = (
        ('released', 'Released'),
        ('suspended', 'Suspended'),
        ('draft', 'Draft'),
    )
    state = models.CharField(choices=StateChoices,
                             default='draft',
                             max_length=10)

    email = models.EmailField(blank=True,
                              null=True)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='Contract')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_contract_id_account'),
            UniqueConstraint(fields=['bidding', 'number', 'account'], name='unique_contract_bidding_number_account_account'),
        ]
        indexes = [
            models.Index(fields=['date_start']),
            models.Index(fields=['-date_start']),
            models.Index(fields=['date_finish']),
            models.Index(fields=['-date_finish']),
            models.Index(fields=['number']),
            models.Index(fields=['state']),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class ContractFile(TenantModel):
    def validate_file_size(field_file):
        file_size = field_file.file.size
        megabyte_limit = 15.0
        if file_size > megabyte_limit*1024*1024:
            raise ValidationError('Max file size is 15MB')


    def upload_to_path(self, filename):
        ext = filename.split('.')[-1]
        name = uuid.uuid4().hex
        return 'contract/{}.{}'.format(name, ext)

    file = models.FileField(upload_to=upload_to_path,
                           blank=True,
                           null=True,
                           validators=[validate_file_size])

    name = models.TextField(blank=False,
                            null=False)

    contract = TenantForeignKey(Contract,
                              on_delete=models.CASCADE,
                              blank=False,
                              null=False,
                              related_name="file")

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='ContractFile')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_contract_file_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class ContractItem(TenantModel):
    contract = TenantForeignKey(Contract,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name="items")

    reference = TenantForeignKey(BiddingItem,
                                  on_delete=models.PROTECT,
                                  blank=False,
                                  null=False)

    ItemTypeChoices = (
        ('unit', 'Unit'),
        ('compound', 'Compound'),
        ('lote', 'Lote'),
    )
    type = models.CharField(choices=ItemTypeChoices, max_length=10)

    parent = TenantForeignKey("self",
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               related_name="items")

    cost = models.DecimalField(decimal_places=2,
                               max_digits=20,
                               default=0.01,
                               null=False,
                               blank=False)

    name = models.CharField(max_length=100,
                            blank=True,
                            null=True)

    description = models.TextField(null=True,
                                   blank=True)


    number = models.PositiveIntegerField(blank=True,
                                         null=True)

    quantity = models.PositiveIntegerField(blank=False,
                                           null=False)

    fixed_cost = models.DecimalField(decimal_places=2,
                                     max_digits=20,
                                     default=0.01,
                                     null=False,
                                     blank=False)

    freight = models.DecimalField(decimal_places=2,
                                  max_digits=20,
                                  default=0.01,
                                  null=False,
                                  blank=False)

    fob_freight = models.DecimalField(decimal_places=2,
                                  max_digits=20,
                                  null=True,
                                  blank=True)

    margin_min = models.DecimalField(decimal_places=2,
                                     max_digits=20,
                                     default=0.01,
                                     null=False,
                                     blank=False)

    price = models.DecimalField(decimal_places=2,
                                max_digits=20,
                                default=0.01,
                                null=False,
                                blank=False)

    price_min = models.DecimalField(decimal_places=2,
                                    max_digits=20,
                                    default=0.01,
                                    null=False,
                                    blank=False)

    tax = models.DecimalField(decimal_places=2,
                              max_digits=20,
                              default=0.01,
                              null=False,
                              blank=False)

    observation = models.TextField(null=True,
                                   blank=True)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='ContractItem')

    def clean(self):
        if (self.type != 'lote'):
            if ContractItem.objects.filter(contract=self.contract, parent=self.parent, number=self.number).exclude(id=self.id).exists():
                raise ValidationError('The fields contract, number must make a unique set.')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_contract_item_id_account'),
            UniqueConstraint(fields=['contract', 'reference', 'account'], name='unique_contract_item_contract_reference_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class ContractItemCompound(TenantModel):
    item = TenantForeignKey(ContractItem,
                             on_delete=models.CASCADE,
                             blank=False,
                             null=False,
                             related_name="product_list")

    reference = TenantForeignKey(BiddingItemCompound,
                                  on_delete=models.PROTECT,
                                  blank=False,
                                  null=False)

    product = TenantForeignKey(Product,
                                on_delete=models.PROTECT,
                                blank=False,
                                null=False)

    price = models.DecimalField(decimal_places=2,
                               max_digits=20,
                               default=0.01,
                               null=False,
                               blank=False)

    quantity = models.PositiveIntegerField(blank=False,
                                           null=False)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='ContractItemCompound')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_contract_item_compound_id_account'),
            UniqueConstraint(fields=['item', 'reference', 'product', 'account'], name='unique_contract_item_compound_item_reference_product_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

