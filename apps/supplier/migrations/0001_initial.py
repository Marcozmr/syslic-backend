

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_cpf_cnpj.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('name_fantasy', models.CharField(blank=True, max_length=100, null=True)),
                ('cnpj', django_cpf_cnpj.fields.CNPJField(blank=True, max_length=50, null=True)),
                ('ie', models.CharField(blank=True, max_length=50, null=True)),
                ('im', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format:'(99) 99999-9999'. Up to 15 digits allowed.", regex='^\\(\\d{2,}\\) \\d{4,5}\\-\\d{4}$')])),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('neighborhood', models.CharField(blank=True, max_length=50, null=True)),
                ('number', models.CharField(blank=True, max_length=50, null=True)),
                ('complement', models.CharField(blank=True, max_length=255, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=50, null=True)),
                ('pix_key', models.CharField(blank=True, max_length=100, null=True)),
                ('account_owner', models.CharField(blank=True, max_length=100, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('bank_agency', models.CharField(blank=True, max_length=30, null=True)),
                ('bank_account', models.CharField(blank=True, max_length=30, null=True)),
                ('address_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='address.addresstype')),
                ('category', models.ManyToManyField(blank=True, to='supplier.Category')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='address.city')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='address.country')),
                ('neighborhood_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='address.neighborhoodtype')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.profile')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='address.state')),
            ],
        ),
    ]
