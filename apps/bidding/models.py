import uuid
import jsonschema
from jsonschema import validate
from django.db import models
from django.db.models import UniqueConstraint

from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from django_multitenant.models import TenantModel
from django_multitenant.mixins import TenantManagerMixin
from django_multitenant.fields import TenantForeignKey

from apps.client.models import (
    Client,
)

from apps.company.models import (
    Company,
    CompanyCertificate,
    CompanyFile,
)

from apps.accounts.models import (
    Profile,
)

from apps.product.models import (
    Product,
)
from apps.address.models import (
        Country,
        State,
        City,
)

from apps.transport.models import (
    Freight,
)

from apps.accounts.models import (
    Account,
    AccountTenantManager,
)

from apps.utils.phone_validator import phone_regex


class BiddingType(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='bidding_type')

    history = HistoricalRecords()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_bidding_type_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_bidding_type_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class Modality(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=100,f
                            blank=False,
                            null=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='bidding_modality')

    history = HistoricalRecords()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_bidding_modality_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_bidding_modality_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class Interest(TenantModel):
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
                                related_name='bidding_interest')

    history = HistoricalRecords()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_bidding_interest_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_bidding_interest_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class Platform(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    link = models.TextField(blank=True,
                            null=True)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='bidding_platform')

    history = HistoricalRecords()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_bidding_platform_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_bidding_platform_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class PlatformLogin(TenantModel):
    company = TenantForeignKey(Company,
                                on_delete=models.PROTECT,
                                blank=False,
                                null=False)
    
    login = models.CharField(max_length=100,
                             blank=True,
                             null=True)

    password = models.CharField(max_length=100,
                                blank=True,
                                null=True)

    observation = models.TextField(null=True,
                                   blank=True)

    received_email = models.BooleanField(default=False)

    platform = TenantForeignKey(Platform,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name="logins")

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='BiddingPlatformLogin')

    class Meta:
        unique_together = (
            'id',
            'account',
        )

    class TenantMeta:
        tenant_field_name = "account_id"

class Phase(TenantModel):
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
                                related_name='bidding_phase')

    history = HistoricalRecords()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_bidding_phase_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_bidding_phase_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class Status(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    color = models.CharField(max_length=100,
                             blank=False,
                             null=False)

    phase = TenantForeignKey(Phase,
                              on_delete=models.CASCADE,
                              blank=False,
                              null=False,
                              related_name="status")

    initial = models.BooleanField(default=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='bidding_status')

    history = HistoricalRecords()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_bidding_status_id_account'),
            UniqueConstraint(fields=['name', 'phase', 'account'], name='unique_bidding_status_name_phase_account'),
        ]
        indexes = [
            models.Index(fields=['account', 'id']),
            models.Index(fields=['account', 'phase']),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class Dispute(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='bidding_dispute')

    history = HistoricalRecords()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_bidding_dispute_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_bidding_dispute_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class Requirement(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='bidding_requirement')

    history = HistoricalRecords()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_bidding_requirement_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_bidding_requirement_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class Bidding(TenantModel):
    client = models.ForeignKey(Client,
                               on_delete=models.PROTECT,
                               blank=False,
                               null=False,
                               related_name="bidding")

    company = models.ForeignKey(Company,
                                on_delete=models.PROTECT,
                                blank=True,
                                null=True,
                                related_name="bidding")

    type = models.ForeignKey(BiddingType,
                             on_delete=models.PROTECT,
                             blank=False,
                             null=False)

    modality = models.ForeignKey(Modality,
                                 on_delete=models.PROTECT,
                                 blank=False,
                                 null=False)

    platform = models.ForeignKey(Platform,
                                 on_delete=models.PROTECT,
                                 blank=False,
                                 null=False)

    interest = models.ForeignKey(Interest,
                                 on_delete=models.PROTECT,
                                 blank=False,
                                 null=False)

    status = models.ForeignKey(Status,
                               on_delete=models.PROTECT,
                               blank=False,
                               null=False)

    phase = models.ForeignKey(Phase,
                              on_delete=models.PROTECT,
                              blank=False,
                              null=False)

    owner = models.ForeignKey(Profile,
                              on_delete=models.PROTECT,
                              blank=True,
                              null=True)

    trade_number = models.CharField(max_length=100,
                                    blank=False,
                                    null=False)

    uasg = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    link_trade = models.CharField(max_length=1000,
                                  blank=True,
                                  null=False)

    link_support = models.CharField(max_length=1000,
                                    blank=True,
                                    null=False)

    link_pncp = models.CharField(max_length=1000,
                                 default=' ',
                                 blank=True,
                                 null=True)

    date = models.DateField(null=True, blank=True)

    bidding_hour = models.TimeField(null=True, blank=True)

    freight_group = models.ForeignKey(Freight,
                                      on_delete=models.PROTECT,
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

    dispute = TenantForeignKey(Dispute,
                                on_delete=models.PROTECT,
                                blank=False,
                                null=False)

    date_capture = models.DateField(null=True,
                                    blank=True)

    date_proposal = models.DateField(null=True,
                                     blank=True)

    hour_proposal = models.TimeField(null=True,
                                     blank=True)

    date_impugnment = models.DateField(null=True,
                                       blank=True)

    date_clarification = models.DateField(null=True,
                                          blank=True)

    price_record_expiration_date = models.DateField(null=True,
                                           blank=True)

    payment_term = models.CharField(max_length=100,
                                    blank=True,
                                    null=True)

    warranty_term = models.CharField(max_length=100,
                                     blank=True,
                                     null=True)

    deadline = models.CharField(max_length=100,
                                blank=True,
                                null=True)

    proposal_validity = models.CharField(max_length=1000,
                                         blank=True,
                                         null=True)

    additional_address = models.CharField(max_length=255,
                                          blank=True,
                                          null=True)

    additional_neighborhood = models.CharField(max_length=50,
                                               blank=True,
                                               null=True)

    additional_number = models.CharField(max_length=50,
                                         blank=True,
                                         null=True)

    additional_complement = models.CharField(max_length=255,
                                             blank=True,
                                             null=True)

    additional_city = models.ForeignKey(City,
                                        related_name='additional_city',
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        null=True)

    additional_state = models.ForeignKey(State,
                                         related_name='additional_state',
                                         on_delete=models.CASCADE,
                                         blank=True,
                                         null=True)

    additional_country = models.ForeignKey(Country,
                                           related_name='additional_country',
                                           on_delete=models.CASCADE,
                                           blank=True,
                                           null=True)

    additional_zip_code = models.CharField(max_length=50,
                                           blank=True,
                                           null=True)

                                                    
    crier = models.CharField(max_length=100,
                             blank=True,
                             null=True)

    phone_number = models.CharField(verbose_name="phone",
                                    validators=[phone_regex],
                                    max_length=17,
                                    blank=True,
                                    null=True)

    email = models.EmailField(blank=True,
                              null=True)

    exclusive_me_epp = models.BooleanField(default=False)

    price_registry = models.BooleanField(default=False)

    observation = models.TextField(null=True,
                                   blank=True)

    requirements = models.JSONField(default=list, null=True, blank=True)

    is_homologated = models.BooleanField(default=False)
    
    imported = models.BooleanField(default=False)

    object_bidding = models.TextField(null=True,
                                      blank=True)
    
    is_filed = models.BooleanField(default=False)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='Bidding')
    def clean(self):
      schema = {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "requirement": {
              "type": "string",
            },
            "status": {
              "type": "boolean",
            },
          },
          "required": ["requirement", "status"],
          "additionalProperties": False,
        },
        "additionalProperties": False,
      }

      try:
        validate(instance=self.requirements, schema=schema)
      except jsonschema.exceptions.ValidationError as e:
        raise ValidationError(e)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_bidding_id_account'),
            UniqueConstraint(fields=['uasg', 'trade_number', 'account'], name='unique_bidding_ruasg_tradenumber_account'),
        ]
        indexes = [
            models.Index(fields=['account']),
            models.Index(fields=['account', 'trade_number']),
            models.Index(fields=['account', 'uasg']),
            models.Index(fields=['account', 'date']),
            models.Index(fields=['account', '-date']),
            models.Index(fields=['account', 'bidding_hour']),
            models.Index(fields=['account', 'date_capture']),
            models.Index(fields=['account', 'date_proposal']),
            models.Index(fields=['account', 'hour_proposal']),
            models.Index(fields=['account', 'is_homologated']),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class BiddingItem(TenantModel):
    ItemTypeChoices = (
        ('unit', 'Unit'),
        ('compound', 'Compound'),
        ('lote', 'Lote'),
    )
    type = models.CharField(choices=ItemTypeChoices, max_length=10)

    bidding = TenantForeignKey(Bidding,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name="items")

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

    ResultChoices = (
        ('gain', 'Ganho'),
        ('lost', 'Perdido'),
        ('pending', 'Pendente'),
    )
    result = models.CharField(choices=ResultChoices,
                              max_length=10,
                              null=False,
                              blank=False,
                              default='pending')

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='BiddingItem')

    def clean(self):
        if (self.type != 'lote'):
            if BiddingItem.objects.filter(bidding=self.bidding, parent=self.parent, number=self.number).exclude(id=self.id).exists():
                raise ValidationError('The fields bidding, number must make a unique set.')

    class Meta:
        unique_together = (
            'id',
            'account',
        )

    class TenantMeta:
        tenant_field_name = "account_id"

class BiddingItemCompound(TenantModel):
    item = TenantForeignKey(BiddingItem,
                             on_delete=models.CASCADE,
                             blank=False,
                             null=False,
                             related_name="product_list")

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
                                related_name='BiddingItemCompound')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_biddingitemcompound_id_account'),
            UniqueConstraint(fields=['item', 'product', 'account'], name='unique_biddingitemcompound_item_prod_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class BiddingFilter(TenantModel):
    name = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    client = TenantForeignKey(Client,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True,
                               related_name="bidding_filter")

    company = TenantForeignKey(Company,
                                on_delete=models.PROTECT,
                                blank=True,
                                null=True,
                                related_name="bidding_filter")

    type = TenantForeignKey(BiddingType,
                             on_delete=models.PROTECT,
                             blank=True,
                             null=True,
                             related_name="bidding_filter")

    modality = TenantForeignKey(Modality,
                                 on_delete=models.PROTECT,
                                 blank=True,
                                 null=True,
                                 related_name="bidding_filter")

    platform = TenantForeignKey(Platform,
                                 on_delete=models.PROTECT,
                                 blank=True,
                                 null=True,
                                 related_name="bidding_filter")

    freight_group = TenantForeignKey(Freight,
                                      on_delete=models.PROTECT,
                                      blank=True,
                                      null=True)

    dispute = TenantForeignKey(Dispute,
                                on_delete=models.PROTECT,
                                blank=True,
                                null=True)

    interest = TenantForeignKey(Interest,
                                 on_delete=models.PROTECT,
                                 blank=True,
                                 null=True,
                                 related_name="bidding_filter")

    status = TenantForeignKey(Status,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True,
                               related_name="bidding_filter")

    phase = TenantForeignKey(Phase,
                              on_delete=models.PROTECT,
                              blank=True,
                              null=True,
                              related_name="bidding_filter")

    owner = models.ForeignKey(Profile,
                              on_delete=models.PROTECT,
                              blank=True,
                              null=True,
                              related_name="bidding_filter")

    date_start = models.DateField(null=True,
                                  blank=True)

    date_finish = models.DateField(null=True,
                                   blank=True)

    date_capture = models.DateField(null=True,
                                    blank=True)

    date_proposal = models.DateField(null=True,
                                     blank=True)

    hour_proposal = models.TimeField(null=True,
                                     blank=True)

    date_impugnment = models.DateField(null=True,
                                       blank=True)

    date_clarification = models.DateField(null=True,
                                          blank=True)

    payment_term = models.CharField(max_length=100,
                                    blank=True,
                                    null=True)

    warranty_term = models.CharField(max_length=100,
                                     blank=True,
                                     null=True)

    deadline = models.CharField(max_length=100,
                                blank=True,
                                null=True)

    is_homologated = models.BooleanField(default=False)

    imported = models.BooleanField(null=True, default=None)

    is_filed = models.BooleanField(null=True, default=False)

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='BiddingFilter')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_biddingfilter_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_biddingfilter_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class BiddingFile(TenantModel):
    def validate_file_size(field_file):
        file_size = field_file.file.size
        megabyte_limit = 15.0
        if file_size > megabyte_limit*1024*1024:
            raise ValidationError('Max file size is 15MB')


    def upload_to_path(self, filename):
        ext = filename.split('.')[-1]
        name = uuid.uuid4().hex
        return 'bidding/{}.{}'.format(name, ext)

    file = models.FileField(upload_to=upload_to_path,
                            blank=True,
                            null=True,
                            validators=[validate_file_size])

    name = models.TextField(null=False,
                            blank=False)

    bidding = TenantForeignKey(Bidding,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name="file")
    
    source = models.CharField(max_length=100,
                              blank=True,
                              null=True,
                              default='bidding')

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='BiddingFile')

    class Meta:
        unique_together = (
            'id',
            'account',
        )

    class TenantMeta:
        tenant_field_name = "account_id"

class BiddingImported(TenantModel):
    cnpj = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    year = models.CharField(max_length=100,
                            blank=False,
                            null=False)

    seq = models.CharField(max_length=100,
                           blank=False,
                           null=False)

    bidding = TenantForeignKey(Bidding,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='BiddingImported')

    history = HistoricalRecords()

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='BiddingImported')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_biddingimported_id_account'),
            UniqueConstraint(fields=['cnpj', 'year', 'seq', 'account'], name='unique_biddingimported_cnpj_year_seq_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class BiddingCompanyFile(TenantModel):    
    document = TenantForeignKey(CompanyFile,
                               on_delete=models.PROTECT,
                               blank=False,
                               null=False)

    bidding = TenantForeignKey(Bidding,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='BiddingCompanyFile')

    class Meta:
        unique_together = (
            'id',
            'account',
        )

    class TenantMeta:
        tenant_field_name = "account_id"

class BiddingCompanyCertificate(TenantModel):    
    document = TenantForeignKey(CompanyCertificate,
                                 on_delete=models.PROTECT,
                                 blank=False,
                                 null=False)

    bidding = TenantForeignKey(Bidding,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name="BiddingCompanyCertificate")

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='BiddingCompanyCertificate')

    class Meta:
        unique_together = (
            'id',
            'account',
        )

    class TenantMeta:
        tenant_field_name = "account_id"
