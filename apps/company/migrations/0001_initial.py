

import apps.company.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_cpf_cnpj.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corporate_name', models.CharField(max_length=100)),
                ('name_fantasy', models.CharField(max_length=100)),
                ('cnpj', django_cpf_cnpj.fields.CNPJField(max_length=50, unique=True, verbose_name='cnpj')),
                ('ie', models.CharField(blank=True, max_length=50, null=True)),
                ('im', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format:'(99) 99999-9999'. Up to 15 digits allowed.", regex='^\\(\\d{2,}\\) \\d{4,5}\\-\\d{4}$')])),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('neighborhood', models.CharField(blank=True, max_length=50, null=True)),
                ('number', models.CharField(blank=True, max_length=50, null=True)),
                ('complement', models.CharField(blank=True, max_length=255, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=50, null=True)),
                ('margin_min', models.DecimalField(decimal_places=2, default=0.01, max_digits=20)),
                ('fixed_cost', models.DecimalField(decimal_places=2, default=0.01, max_digits=20)),
                ('tax_aliquot', models.DecimalField(decimal_places=2, default=0.01, max_digits=20)),
                ('address_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.addresstype')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.city')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.country')),
                ('neighborhood_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.neighborhoodtype')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.state')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyFileStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
            ],
            options={
                'unique_together': {('name',)},
            },
        ),
        migrations.CreateModel(
            name='CompanyFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=apps.company.models.CompanyFile.upload_to_path, validators=[apps.company.models.CompanyFile.validate_file_size])),
                ('file_name', models.CharField(max_length=100)),
                ('document_name', models.CharField(max_length=100)),
                ('annotation', models.CharField(blank=True, max_length=100)),
                ('date_emission', models.DateField()),
                ('date_validity', models.DateField()),
                ('link_certificates', models.CharField(blank=True, max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_file', to='company.company')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company.companyfilestatus')),
            ],
        ),
    ]
