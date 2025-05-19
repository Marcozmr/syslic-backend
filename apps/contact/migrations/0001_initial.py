

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
        ('address', '0001_initial'),
        ('supplier', '0001_initial'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format:'(99) 99999-9999'. Up to 15 digits allowed.", regex='^\\(\\d{2,}\\) \\d{4,5}\\-\\d{4}$')])),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('neighborhood', models.CharField(blank=True, max_length=50, null=True)),
                ('number', models.CharField(blank=True, max_length=50, null=True)),
                ('complement', models.CharField(blank=True, max_length=255, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=50, null=True)),
                ('position', models.CharField(blank=True, max_length=50, null=True)),
                ('sector', models.CharField(blank=True, max_length=50, null=True)),
                ('address_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='address.addresstype')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='address.city')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contacts', to='client.client')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contacts', to='company.company')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='address.country')),
                ('neighborhood_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='address.neighborhoodtype')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='address.state')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contacts', to='supplier.supplier')),
            ],
        ),
    ]
