

import apps.bidding.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        ('product', '__first__'),
        ('accounts', '0001_initial'),
        ('transport', '__first__'),
        ('client', '0001_initial'),
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bidding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_number', models.CharField(max_length=100)),
                ('uasg', models.CharField(max_length=100)),
                ('link_trade', models.CharField(blank=True, max_length=1000)),
                ('link_support', models.CharField(blank=True, max_length=1000)),
                ('date', models.DateField()),
                ('bidding_hour', models.TimeField(blank=True, null=True)),
                ('date_capture', models.DateField(blank=True, null=True)),
                ('date_proposal', models.DateField(blank=True, null=True)),
                ('hour_proposal', models.TimeField(blank=True, null=True)),
                ('date_impugnment', models.DateField(blank=True, null=True)),
                ('date_clarification', models.DateField(blank=True, null=True)),
                ('payment_term', models.DateField(blank=True, null=True)),
                ('warranty_term', models.DateField(blank=True, null=True)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('proposal_validity', models.CharField(blank=True, max_length=1000, null=True)),
                ('additional_address', models.CharField(blank=True, max_length=255, null=True)),
                ('additional_neighborhood', models.CharField(blank=True, max_length=50, null=True)),
                ('additional_number', models.CharField(blank=True, max_length=50, null=True)),
                ('additional_complement', models.CharField(blank=True, max_length=255, null=True)),
                ('additional_zip_code', models.CharField(blank=True, max_length=50, null=True)),
                ('crier', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format:'(99) 99999-9999'. Up to 15 digits allowed.", regex='^\\(\\d{2,}\\) \\d{4,5}\\-\\d{4}$')], verbose_name='phone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('exclusive_me_epp', models.BooleanField(default=False)),
                ('price_registry', models.BooleanField(default=False)),
                ('observation', models.TextField(blank=True, null=True)),
                ('requirements', models.JSONField(blank=True, default=list, null=True)),
                ('additional_city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='additional_city', to='address.city')),
                ('additional_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='additional_country', to='address.country')),
                ('additional_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='additional_state', to='address.state')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.city')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bidding', to='client.client')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bidding', to='company.company')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.country')),
            ],
        ),
        migrations.CreateModel(
            name='BiddingItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('unit', 'Unit'), ('compound', 'Compound'), ('lote', 'Lote')], max_length=10)),
                ('cost', models.DecimalField(decimal_places=2, default=0.01, max_digits=20)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('number', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('fixed_cost', models.DecimalField(decimal_places=2, default=0.01, max_digits=20)),
                ('freight', models.DecimalField(decimal_places=2, default=0.01, max_digits=20)),
                ('margin_min', models.DecimalField(decimal_places=2, default=0.01, max_digits=20)),
                ('price', models.DecimalField(decimal_places=2, default=0.01, max_digits=20)),
                ('price_min', models.DecimalField(decimal_places=2, default=0.01, max_digits=20)),
                ('tax', models.DecimalField(decimal_places=2, default=0.01, max_digits=20)),
                ('bidding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='bidding.bidding')),
            ],
            options={
                'unique_together': {('bidding', 'number')},
            },
        ),
        migrations.CreateModel(
            name='Dispute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('color', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Modality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('color', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
                ('login', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('received_email', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('initial', models.BooleanField(default=False)),
                ('phase', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='status', to='bidding.phase')),
            ],
            options={
                'unique_together': {('name', 'phase')},
            },
        ),
        migrations.CreateModel(
            name='BiddingFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('date_start', models.DateField(blank=True, null=True)),
                ('date_finish', models.DateField(blank=True, null=True)),
                ('date_capture', models.DateField(blank=True, null=True)),
                ('date_proposal', models.DateField(blank=True, null=True)),
                ('hour_proposal', models.TimeField(blank=True, null=True)),
                ('date_impugnment', models.DateField(blank=True, null=True)),
                ('date_clarification', models.DateField(blank=True, null=True)),
                ('payment_term', models.DateField(blank=True, null=True)),
                ('warranty_term', models.DateField(blank=True, null=True)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bidding_filter', to='client.client')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bidding_filter', to='company.company')),
                ('dispute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bidding.dispute')),
                ('freight_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='transport.freight')),
                ('interest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bidding_filter', to='bidding.interest')),
                ('modality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bidding_filter', to='bidding.modality')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bidding_filter', to='accounts.profile')),
                ('phase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bidding_filter', to='bidding.phase')),
                ('platform', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bidding_filter', to='bidding.platform')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bidding_filter', to='bidding.status')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bidding_filter', to='bidding.type')),
            ],
        ),
        migrations.CreateModel(
            name='BiddingFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=apps.bidding.models.BiddingFile.upload_to_path, validators=[apps.bidding.models.BiddingFile.validate_file_size])),
                ('name', models.CharField(max_length=100)),
                ('bidding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file', to='bidding.bidding')),
            ],
        ),
        migrations.AddField(
            model_name='bidding',
            name='dispute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bidding.dispute'),
        ),
        migrations.AddField(
            model_name='bidding',
            name='freight_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='transport.freight'),
        ),
        migrations.AddField(
            model_name='bidding',
            name='interest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bidding.interest'),
        ),
        migrations.AddField(
            model_name='bidding',
            name='modality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bidding.modality'),
        ),
        migrations.AddField(
            model_name='bidding',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.profile'),
        ),
        migrations.AddField(
            model_name='bidding',
            name='platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bidding.platform'),
        ),
        migrations.AddField(
            model_name='bidding',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.state'),
        ),
        migrations.AddField(
            model_name='bidding',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bidding.status'),
        ),
        migrations.AddField(
            model_name='bidding',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bidding.type'),
        ),
        migrations.CreateModel(
            name='BiddingItemCompound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.01, max_digits=20)),
                ('quantity', models.PositiveIntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_list', to='bidding.biddingitem')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product')),
            ],
            options={
                'unique_together': {('item', 'product')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='bidding',
            unique_together={('trade_number', 'uasg')},
        ),
    ]
