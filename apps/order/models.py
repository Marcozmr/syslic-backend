import uuid
from django.apps import apps
from django.db import models
from django.db.models import Sum, F
from django.db.models import UniqueConstraint
from apps.utils.phone_validator import phone_regex
from simple_history.models import HistoricalRecords

from django_multitenant.models import TenantModel
from django_multitenant.fields import TenantForeignKey

from apps.contract.models import (
    Contract,
    ContractItem,
    ContractItemCompound,
)

from apps.company.models import (
    Company,
)

from apps.client.models import (
    Client,
)

from apps.product.models import (
    Product,
)

from apps.transport.models import (
    Carrier,
)

from apps.accounts.models import (
    Profile,
    Account,
    AccountTenantManager,
)

from apps.address.models import (
        Country,
        State,
        City,
)

from .managers import (
    OrderAuditPercentageManager,
)

class OrderInterest(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    color = models.CharField(max_length=100,
                             blank=False,
                             null=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='order_interest')

    history = HistoricalRecords()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_interest_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_order_interest_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class Order(TenantModel):
    contract = models.OneToOneField(Contract,
                                   related_name='order',
                                   on_delete=models.PROTECT,
                                   blank=False,
                                   null=False)

    interest = TenantForeignKey(OrderInterest,
                               on_delete=models.PROTECT,
                               blank=False,
                               null=False)

    company = TenantForeignKey(Company,
                                on_delete=models.PROTECT,
                                blank=True,
                                null=True)

    owner = models.ForeignKey(Profile,
                              on_delete=models.PROTECT,
                              blank=True,
                              null=True)

    date_expiration = models.DateField(null=True, blank=True)

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
                             related_name='city',
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)

    state = models.ForeignKey(State,
                              related_name='state',
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True)

    country = models.ForeignKey(Country,
                                related_name='country',
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)

    zip_code = models.CharField(max_length=50,
                                blank=True,
                                null=True)


    nf_payed = models.BooleanField(default=False)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='Order')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_id_account'),
            UniqueConstraint(fields=['contract', 'account'], name='unique_order_contract_account'),
        ]
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['-id']),
            models.Index(fields=['date_expiration']),
            models.Index(fields=['-date_expiration']),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderFilter(TenantModel):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    uasg = models.CharField(max_length=100,
                                    blank=True,
                                    null=True)

    trade_number = models.CharField(max_length=100,
                                    blank=True,
                                    null=True)

    client = TenantForeignKey(Client,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True,
                               related_name="order_filter")

    company = TenantForeignKey(Company,
                                on_delete=models.PROTECT,
                                blank=True,
                                null=True,
                                related_name="order_filter")

    interest = TenantForeignKey(OrderInterest,
                                 on_delete=models.PROTECT,
                                 blank=True,
                                 null=True,
                                 related_name="order_filter")

    date_expiration_gte = models.DateField(null=True,
                                     blank=True)

    date_expiration_lte = models.DateField(null=True,
                                     blank=True)

    owner = models.ForeignKey(Profile,
                              on_delete=models.PROTECT,
                              blank=True,
                              null=True,
                              related_name="order_filter")

    nf_payed = models.BooleanField(null=True)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderFilter')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_filter_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_order_filter_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderFile(TenantModel):
    def validate_file_size(field_file):
        file_size = field_file.file.size
        megabyte_limit = 15.0
        if file_size > megabyte_limit*1024*1024:
            raise ValidationError('Max file size is 15MB')


    def upload_to_path(self, filename):
        ext = filename.split('.')[-1]
        name = uuid.uuid4().hex
        return 'order/{}.{}'.format(name, ext)

    file = models.FileField(upload_to=upload_to_path,
                           blank=True,
                           null=True,
                           validators=[validate_file_size])

    name = models.TextField(blank=False,
                            null=False)

    order = TenantForeignKey(Order,
                              on_delete=models.CASCADE,
                              blank=False,
                              null=False,
                              related_name="file")

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderFile')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_file_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderCommitmentStatus(TenantModel):
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
                                related_name='commitment_status')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_commitment_status_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_order_commitment_status_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderCommitment(TenantModel):
    order = TenantForeignKey(Order,
                              related_name='commitments',
                              on_delete=models.CASCADE,
                              blank=False,
                              null=False)

    company = TenantForeignKey(Company,
                                on_delete=models.PROTECT,
                                blank=False,
                                null=False)

    status = TenantForeignKey(OrderCommitmentStatus,
                               on_delete=models.PROTECT,
                               blank=False,
                               null=False)

    number = models.CharField(max_length=100,
                              blank=False,
                              null=False)

    date_delivery = models.DateField(null=False,
                                     blank=False)

    date_expiration = models.DateField(null=False,
                                       blank=False)

    commitmentSituationChoices = (
        ('idle', 'Idle'),
        ('done', 'Done'),
        ('audit', 'Audit'),
        ('declined', 'Declined'),
    )
    situation = models.CharField(choices=commitmentSituationChoices,
                                 max_length=20,
                                 default='idle')

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderCommitment')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_commitment_id_account'),
            UniqueConstraint(fields=['order', 'number', 'account'], name='unique_order_commitment_order_number_account'),
        ]
        indexes = [
            models.Index(fields=['-id']),
            models.Index(fields=['date_delivery']),
            models.Index(fields=['-date_delivery']),
            models.Index(fields=['date_expiration']),
            models.Index(fields=['-date_expiration']),
            models.Index(fields=['situation']),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderCommitmentFilter(TenantModel):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    status = TenantForeignKey(OrderCommitmentStatus,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True)

    number = models.CharField(max_length=100,
                              blank=True,
                              null=True)

    date_delivery = models.DateField(null=True,
                                     blank=True)

    date_expiration = models.DateField(null=True,
                                       blank=True)

    trade_number = models.CharField(max_length=100,
                                    blank=True,
                                    null=True)

    client = TenantForeignKey(Client,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True)

    note_number = models.CharField(max_length=100,
                                   blank=True,
                                   null=True)

    billing_date = models.DateField(null=True,
                                    blank=True)

    pay_date = models.DateField(null=True,
                                blank=True)

    real_pay_date = models.DateField(null=True,
                                     blank=True)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderCommitmentFilter')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_commitment_filter_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_order_commitment_filter_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderCommitmentItem(TenantModel):
    commitment = TenantForeignKey(OrderCommitment,
                              related_name='items',
                              on_delete=models.CASCADE,
                              blank=False,
                              null=False)

    item = TenantForeignKey(ContractItem,
                             on_delete=models.PROTECT,
                             blank=False,
                             null=False)

    quantity = models.PositiveIntegerField(blank=False,
                                           null=False)

    annotation = models.TextField(null=True,
                                  blank=True)

    deliverable = models.BooleanField(default=False)

    last_audit_margin = models.DecimalField(decimal_places=2,
                                             max_digits=20,
                                             default=0.00)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderCommitmentItem')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_commitment_item_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderCommitmentItemProduct(TenantModel):
    item = TenantForeignKey(OrderCommitmentItem,
                              related_name='products',
                              on_delete=models.CASCADE,
                              blank=False,
                              null=False)

    product = TenantForeignKey(ContractItemCompound,
                             on_delete=models.PROTECT,
                             blank=False,
                                           null=False)

    cost = models.DecimalField(decimal_places=2,
                               max_digits=20,
                               default=0.01,
                               null=False,
                               blank=False)
    
    fob_freight = models.DecimalField(decimal_places=2,
                               max_digits=20,
                               default=0.00,
                               null=False,
                               blank=False)

    last_audit_value = models.DecimalField(decimal_places=2,
                                           max_digits=20,
                                           default=0.00)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderCommitmentItemProduct')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_commitment_item_product_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderCommitmentFile(TenantModel):
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

    commitment = TenantForeignKey(OrderCommitment,
                                   on_delete=models.CASCADE,
                                   blank=False,
                                   null=False,
                                   related_name="file")

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderCommitmentFile')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_commitment_file_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderDeliveryStatus(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    color = models.CharField(max_length=100,
                             blank=False,
                             null=False)

    initial = models.BooleanField(default=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='delivery_status')

    history = HistoricalRecords()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_delivery_status_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_order_delivery_status_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderDeliveryFilter(TenantModel):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)
    
    delivery_number = models.CharField(max_length=100,
                                       blank=True,
                                       null=True)
    
    client = TenantForeignKey(Client,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True)

    trade_number = models.CharField(max_length=100,
                                    blank=True,
                                    null=True)

    company = TenantForeignKey(Company,
                                on_delete=models.PROTECT,
                                blank=True,
                                null=True)

    carrier = TenantForeignKey(Carrier,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True)

    status = TenantForeignKey(OrderDeliveryStatus,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True)
    
    date_delivery = models.DateField(null=True,
                                     blank=True)

    invoicing_delivery_date = models.DateField(null=True,
                                               blank=True)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderDeliveryFilter')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_delivery_filter_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_order_delivery_filter_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderDelivery(TenantModel):
    order = TenantForeignKey(Order,
                             on_delete=models.CASCADE,
                             blank=False,
                             null=False)

    company = TenantForeignKey(Company,
                                on_delete=models.PROTECT,
                                blank=False,
                                null=False)

    status = TenantForeignKey(OrderDeliveryStatus,
                               on_delete=models.PROTECT,
                               blank=False,
                               null=False)

    date_delivery = models.DateField(null=True,
                                     blank=True)

    carrier = TenantForeignKey(Carrier,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True)

    freight_cost = models.DecimalField(decimal_places=2,
                               max_digits=20,
                               default=0.01,
                               null=True,
                               blank=True)

    annotation = models.TextField(null=True,
                                  blank=True)

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

    expedition_date = models.DateField(null=True,
                                       blank=True)
     
    invoicing_delivery_date = models.DateField(null=True,
                                               blank=True)

    driver_name = models.CharField(max_length=100,
                                       blank=True,
                                       null=True)

    DeliverySituationChoices = (
        ('idle', 'Idle'),
        ('invoicing', 'Invoicing'),
        ('released', 'Released'),
        ('declined', 'Declined'),
        ('audit', 'Audit'),
        ('done', 'Done'),
    )
    situation = models.CharField(choices=DeliverySituationChoices,
                                 max_length=20,
                                 default='idle')
    
    last_audit_value = models.DecimalField(decimal_places=2,
                                           max_digits=20,
                                           default=0.00)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderDelivery')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_delivery_id_account'),
        ]
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['-id']),
            models.Index(fields=['date_delivery']),
            models.Index(fields=['-date_delivery']),
            models.Index(fields=['invoicing_delivery_date']),
            models.Index(fields=['-invoicing_delivery_date']),
            models.Index(fields=['situation']),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderDeliveryFile(TenantModel):
    def validate_file_size(field_file):
        file_size = field_file.file.size
        megabyte_limit = 15.0
        if file_size > megabyte_limit*1024*1024:
            raise ValidationError('Max file size is 15MB')


    def upload_to_path(self, filename):
        ext = filename.split('.')[-1]
        name = uuid.uuid4().hex
        return 'order/delivery/{}.{}'.format(name, ext)

    file = models.FileField(upload_to=upload_to_path,
                           blank=True,
                           null=True,
                           validators=[validate_file_size])

    name = models.TextField(blank=False,
                            null=False)

    delivery = TenantForeignKey(OrderDelivery,
                              on_delete=models.CASCADE,
                              blank=False,
                              null=False,
                              related_name="file")

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderDeliveryFile')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_delivery_file_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderDeliveryItem(TenantModel):
    delivery = TenantForeignKey(OrderDelivery,
                              related_name='items',
                              on_delete=models.CASCADE,
                              blank=False,
                              null=False)

    item = TenantForeignKey(OrderCommitmentItem,
                             related_name='items_delivery',
                             on_delete=models.PROTECT,
                             blank=False,
                             null=False)

    quantity = models.PositiveIntegerField(blank=False,
                                           null=False)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderDeliveryItem')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_delivery_item_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderDeliveryFreightCotation(TenantModel):
    delivery = TenantForeignKey(OrderDelivery,
                              related_name='cotations',
                              on_delete=models.CASCADE,
                              blank=False,
                              null=False)

    carrier = TenantForeignKey(Carrier,
                             on_delete=models.PROTECT,
                             blank=False,
                             null=False)

    email = models.EmailField(blank=True,
                              null=True)


    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=17,
                                    blank=True,
                                    null=True)

    cost = models.DecimalField(decimal_places=2,
                               max_digits=20,
                               default=0.01,
                               null=False,
                               blank=False)

    date_cotation = models.DateField(null=False,
                                     blank=False)

    accepted = models.BooleanField(default=False)

    quote_number = models.CharField(max_length=50,
                                       blank=False,
                                       null=False)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderDeliveryFreightCotation')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_delivery_freight_cotation_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderAssistanceStatus(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    color = models.CharField(max_length=100,
                             blank=False,
                             null=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='assistance_status')

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderAssistanceStatus')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_assistance_status_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_order_assistance_status_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"
    
class OrderAssistanceType(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderAssistanceType')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_assistance_type_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_order_assistance_type_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"
    
class OrderAssistance(TenantModel):
    order= TenantForeignKey(Order,
                             related_name='assistances',
                             on_delete=models.CASCADE,
                             blank=False,
                             null=False)
    
    type = TenantForeignKey(OrderAssistanceType,
                              on_delete=models.PROTECT,
                              blank=False,
                              null=False)
    
    status = TenantForeignKey(OrderAssistanceStatus,
                              on_delete=models.PROTECT,
                              blank=False,
                              null=False)
    
    product = TenantForeignKey(Product, 
                                on_delete=models.PROTECT,
                                blank=False,
                                null=False)
    
    technician_name = models.CharField(max_length=100,
                                       blank=True,
                                       null=True)
    
    technician_phone = models.CharField(validators=[phone_regex],
                                    max_length=17,
                                    blank=True,
                                    null=True)
    
    organ_phone = models.CharField(validators=[phone_regex],
                                    max_length=17,
                                    blank=True,
                                    null=True)
    
    payment_value = models.DecimalField(decimal_places=2,
                               max_digits=20,
                               default=0.01,
                               null=True,
                               blank=True)
    
    date_scheduled = models.DateField(null=True,
                                       blank=True)
    
    comments = models.CharField(max_length=5000,
                               blank=True,
                               null=True)
    
    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderAssistance')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_assistance_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"
    
class OrderAssistanceFilter(TenantModel):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)
    
    client = TenantForeignKey(Client,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True)
    
    type = TenantForeignKey(OrderAssistanceType,
                            on_delete=models.PROTECT,
                            blank=True,
                            null=True)

    status = TenantForeignKey(OrderAssistanceStatus,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True)
    
    date_scheduled_gte = models.DateField(null=True,
                                         blank=True)
    
    date_scheduled_lte = models.DateField(null=True,
                                       blank=True)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderAssistanceFilter')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_assistance_filter_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_order_assistance_filter_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"
    
class OrderAuditPercentage(TenantModel):
    commitment_percentage = models.DecimalField(decimal_places=2,
                                                max_digits=20,
                                                default=0.00,
                                                null=False,
                                                blank=False)
    
    delivery_percentage = models.DecimalField(decimal_places=2,
                                              max_digits=20,
                                              default=0.00,
                                              null=False,
                                              blank=False)
    
    commitment_margin_percentage = models.DecimalField(decimal_places=2,
                                                        max_digits=20,
                                                        default=0.00,
                                                        null=False,
                                                        blank=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='order_audit')
    
    objects = OrderAuditPercentageManager()
    
    history = HistoricalRecords()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_audit_percentage_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderInvoicingStatus(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    color = models.CharField(max_length=100,
                             blank=False,
                             null=False)

    initial = models.BooleanField(default=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='invoicing_status')

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderInvoicingStatus')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_invoicing_status_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_order_invoicing_status_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderInvoicing(TenantModel):
    delivery = TenantForeignKey(OrderDelivery,
                                on_delete=models.PROTECT,
                                blank=False,
                                null=False)

    commitment = TenantForeignKey(OrderCommitment,
                                on_delete=models.PROTECT,
                                blank=False,
                                null=False)

    note_number = models.CharField(max_length=1000,
                                   blank=True,
                                   null=True)
      
    invoicing_date = models.DateField(null=True,
                                      blank=True)

    expected_payment_date = models.DateField(null=True,
                                     blank=True)

    real_pay_date = models.DateField(null=True,
                                     blank=True)

    annotation = models.TextField(null=True,
                                  blank=True)

    status = TenantForeignKey(OrderInvoicingStatus,
                               on_delete=models.PROTECT,
                               blank=False,
                               null=False)

    total_items = models.DecimalField(decimal_places=2,
                                      max_digits=20,
                                      default=0.00,
                                      null=False,
                                      blank=False)

    total_nf = models.DecimalField(decimal_places=2,
                                   max_digits=20,
                                   default=0.00,
                                   null=False,
                                   blank=False)
    
    liquid_margin = models.DecimalField(decimal_places=2,
                                        max_digits=20,
                                        default=0.00,
                                        null=True,
                                        blank=False)
    
    InvoicingSituationChoices = (
        ('idle', 'Idle'),
        ('released', 'Released'),
        ('done', 'Done'),
    )
    situation = models.CharField(choices=InvoicingSituationChoices,
                                 max_length=20,
                                 default='idle')
    
    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderInvoicing')

    def get_model(self, label, model):
        return apps.get_model(app_label=label, model_name=model)

    def get_total_items(self):
        order_commitment_item_model = self.get_model('order', 'OrderCommitmentItem')

        total = order_commitment_item_model.objects.filter(
            commitment=self.commitment,
            items_delivery__delivery=self.delivery
        ).aggregate(
            total=Sum(F('quantity') * F('item__price'), output_field=models.FloatField())
        )['total'] or 0.0

        return total

    def get_total_nf(self):
        order_delivery_item_model = self.get_model('order', 'OrderDeliveryItem')

        total = order_delivery_item_model.objects.filter(
                delivery=self.delivery,
                item__commitment=self.commitment
        ).aggregate(
            total=Sum(F('quantity') * F('item__item__price'), output_field=models.FloatField())
        )['total'] or 0.0

        return total

    def get_liquid_margin(self):
        order_delivery_item_model = self.get_model('order', 'OrderDeliveryItem')
        contract_item_model = self.get_model('contract', 'ContractItem')
        order_commitment_item_model = self.get_model('order', 'OrderCommitmentItemProduct')
        order_delivery_cotation_model = self.get_model('order', 'OrderDeliveryFreightCotation')

        total_invoicing = self.get_total_nf()

        item_delivery_queryset = order_delivery_item_model.objects.filter(delivery=self.delivery)

        total_delivery = 0

        for item_delivery in item_delivery_queryset:
            total_delivery += float(item_delivery.quantity) * float(item_delivery.item.item.price)

        delivery_items_queryset = order_delivery_item_model.objects.filter(delivery=self.delivery, item__commitment=self.commitment)
        delivery_item_first = delivery_items_queryset.first()


        contract_item = contract_item_model.objects.filter(contract=delivery_item_first.item.commitment.order.contract).first()

        tax = float(contract_item.tax)/100 * total_invoicing

        fixed_cost = float(contract_item.fixed_cost)/100 * total_invoicing

        item_cost = 0
        item_fob = 0

        for item in delivery_items_queryset:
            unit_cost = 0
            unit_fob = 0

            products = order_commitment_item_model.objects.filter(item=item.item)
            for item_commitment in products:
                unit_fob += float(item_commitment.fob_freight)
                unit_cost += float(item_commitment.product.quantity) * float(item_commitment.cost)

            item_cost += unit_cost * float(item.quantity)
            item_fob += unit_fob * float(item.quantity)


        freight = 0
        freight_queryset = order_delivery_cotation_model.objects.filter(delivery=self.delivery, accepted=True)
        if not freight_queryset.exists():
            return None

        delivery_freight = freight_queryset.first()
        freight = float(delivery_freight.cost) * (total_invoicing/total_delivery)
       
        total_margin = ((total_invoicing - (item_cost + item_fob + freight + tax + fixed_cost)) / total_invoicing) * 100

        return total_margin
    
    def save(self, *args, **kwargs):
        self.total_items = self.get_total_items()
        self.total_nf = self.get_total_nf()
        self.liquid_margin = self.get_liquid_margin()

        super(OrderInvoicing, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_invoicing_id_account'),
            UniqueConstraint(fields=['delivery', 'commitment', 'account'], name='unique_order_invoicing_delivery_commitment_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderInvoicingFile(TenantModel):
    def validate_file_size(field_file):
        file_size = field_file.file.size
        megabyte_limit = 15.0
        if file_size > megabyte_limit*1024*1024:
            raise ValidationError('Max file size is 15MB')


    def upload_to_path(self, filename):
        ext = filename.split('.')[-1]
        name = uuid.uuid4().hex
        return 'order/invoicing/{}.{}'.format(name, ext)

    file = models.FileField(upload_to=upload_to_path,
                           blank=True,
                           null=True,
                           validators=[validate_file_size])

    name = models.TextField(blank=False,
                            null=False)

    invoicing = TenantForeignKey(OrderInvoicing,
                              on_delete=models.CASCADE,
                              blank=False,
                              null=False,
                              related_name="file")

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderInvoicingFile')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_invoicing_file_id_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class OrderInvoicingFilter(TenantModel):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    delivery_number = models.CharField(max_length=100,
                                       blank=True,
                                       null=True)

    commitment_number = models.CharField(max_length=100,
                                         blank=True,
                                         null=True)

    company = TenantForeignKey(Company,
                                on_delete=models.PROTECT,
                                blank=True,
                                null=True)

    note_number = models.CharField(max_length=100,
                                   blank=True,
                                   null=True)

    carrier = TenantForeignKey(Carrier,
                                on_delete=models.PROTECT,
                                blank=True,
                                null=True)

    client = TenantForeignKey(Client,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True)

    status = TenantForeignKey(OrderInvoicingStatus,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True)

    nf_payed = models.BooleanField(null=True)

    date_delivery_gte = models.DateField(null=True,
                                         blank=True)

    date_delivery_lte = models.DateField(null=True,
                                         blank=True)

    invoicing_delivery_date_gte = models.DateField(null=True,
                                                   blank=True)

    invoicing_delivery_date_lte = models.DateField(null=True,
                                                   blank=True)
      
    real_pay_date_gte = models.DateField(null=True,
                                        blank=True)

    real_pay_date_lte = models.DateField(null=True,
                                        blank=True)

    invoicing_date_gte = models.DateField(null=True,
                                        blank=True)

    invoicing_date_lte = models.DateField(null=True,
                                          blank=True)

    situation = models.CharField(max_length=20,
                                 blank=True,
                                 null=True)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='OrderInvoicingFilter')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_order_invoicing_filter_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_order_invoicing_filter_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"
