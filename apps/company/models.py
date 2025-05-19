import uuid
from django_cpf_cnpj.fields import CNPJField
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

from apps.accounts.models import (
    Account,
    AccountTenantManager,
)

class Company(TenantModel):
    corporate_name = models.CharField(max_length=100)

    name_fantasy = models.CharField(max_length=100)

    cnpj = CNPJField(verbose_name="cnpj",
                     max_length=50,
                     blank=False,
                     null=False)

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
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True)

    address = models.CharField(max_length=255,
                               blank=True,
                               null=True)

    neighborhood_type = models.ForeignKey(NeighborhoodType,
                                     on_delete=models.CASCADE,
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

    margin_min = models.DecimalField(decimal_places=2,
                                     max_digits=20,
                                     default=0.01,
                                     null=False,
                                     blank=False)

    fixed_cost = models.DecimalField(decimal_places=2,
                                     max_digits=20,
                                     default=0.01,
                                     null=False,
                                     blank=False)

    tax_aliquot = models.DecimalField(decimal_places=2,
                                      max_digits=20,
                                      default=0.01,
                                      null=False,
                                      blank=False)

    difference = models.DecimalField(decimal_places=2,
                                      max_digits=20,
                                      default=0.01,
                                      null=False,
                                      blank=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='Company')

    class Meta:
        unique_together = (
            'id',
            'account',
        )
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_company_id_account'),
            UniqueConstraint(fields=['cnpj', 'account'], name='unique_company_cnpj_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class CompanyFile(TenantModel):
    def validate_file_size(field_file):
        file_size = field_file.file.size
        megabyte_limit = 15.0
        if file_size > megabyte_limit*1024*1024:
            raise ValidationError('Max file size is 15MB')


    def upload_to_path(self, filename):
        ext = filename.split('.')[-1]
        name = uuid.uuid4().hex
        return 'company/{}.{}'.format(name, ext)

    file = models.FileField(upload_to=upload_to_path,
                           blank=True,
                           null=True,
                           validators=[validate_file_size])

    file_name = models.TextField(blank=False,
                                 null=False)

    document_name = models.TextField(blank=False,
                                     null=False)

    annotation = models.CharField(max_length=100,
                                     blank=True,
                                     null=False)

    date_emission = models.DateField(null=False, blank=False)

    date_validity = models.DateField(null=False, blank=False)

    link_certificates = models.CharField(max_length=100,
                                         blank=True,
                                         null=False)

    company = TenantForeignKey(Company,
                              on_delete=models.CASCADE,
                              blank=False,
                              null=False,
                              related_name="company_file")

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='CompanyFile')

    class Meta:
        unique_together = (
            'id',
            'account',
        )

    class TenantMeta:
        tenant_field_name = "account_id"

class CompanyCertificateStatus(TenantModel):
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
                                related_name='CompanyCertificateStatus')

    class Meta:
        unique_together = (
            'id',
            'account',
        )
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_company_certificate_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_company_certicate_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class CompanyCertificate(TenantModel):
    company = TenantForeignKey(Company,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name="certificate_company")

    client = TenantForeignKey(Client,
                               on_delete=models.PROTECT,
                               blank=False,
                               null=False,
                               related_name="certificate_client")
    status = TenantForeignKey(CompanyCertificateStatus,
                               on_delete=models.PROTECT,
                               blank=False,
                               null=False,
                               related_name="certificate_status")

    end_authentication = models.CharField(max_length=100,
                                          blank=True,
                                          null=True,
                                         )

    annotation = models.CharField(max_length=100,
                                  blank=True,
                                  null=True,
                                 )

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='CompanyCertificate')

    class Meta:
        unique_together = (
            'id',
            'account',
        )

    class TenantMeta:
        tenant_field_name = "account_id"

class CompanyCertificateFile(TenantModel):
    def validate_file_size(field_file):
        file_size = field_file.file.size
        megabyte_limit = 15.0
        if file_size > megabyte_limit*1024*1024:
            raise ValidationError('Max file size is 15MB')


    def upload_to_path(self, filename):
        ext = filename.split('.')[-1]
        name = uuid.uuid4().hex
        return 'company/certificate/{}.{}'.format(name, ext)


    file = models.FileField(upload_to=upload_to_path,
                            blank=False,
                            null=False,
                            validators=[validate_file_size])

    file_name = models.TextField(blank=False,
                                 null=False)

    certificate = TenantForeignKey(CompanyCertificate,
                                    on_delete=models.CASCADE,
                                    blank=False,
                                    null=False,
                                    related_name="certificate_files")

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='CompanyCertificateFile')

    class Meta:
        unique_together = (
            'id',
            'account',
        )

    class TenantMeta:
        tenant_field_name = "account_id"

