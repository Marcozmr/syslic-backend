

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
        ('accounts', '0001_initial'),
        ('bidding', '0002_auto_20230529_0416'),
        ('company', '0002_auto_20230529_0416'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('color', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('color', models.CharField(max_length=100)),
                ('initial', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_delivery', models.DateField()),
                ('date_expiration', models.DateField()),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('neighborhood', models.CharField(blank=True, max_length=50, null=True)),
                ('number', models.CharField(blank=True, max_length=50, null=True)),
                ('complement', models.CharField(blank=True, max_length=255, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=50, null=True)),
                ('bidding', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bidding.bidding', unique=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city', to='address.city')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company.company')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='country', to='address.country')),
                ('interest', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.orderinterest')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.profile')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='state', to='address.state')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.orderstatus')),
            ],
        ),
    ]
