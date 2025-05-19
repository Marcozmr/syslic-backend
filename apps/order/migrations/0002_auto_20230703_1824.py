

import apps.order.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20230529_0416'),
        ('accounts', '0001_initial'),
        ('bidding', '0003_auto_20230703_1824'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='nf_payed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.01, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='bidding',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='bidding.bidding'),
        ),
        migrations.AlterField(
            model_name='order',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='company.company'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_delivery',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_expiration',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.profile'),
        ),
        migrations.CreateModel(
            name='OrderFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=apps.order.models.OrderFile.upload_to_path, validators=[apps.order.models.OrderFile.validate_file_size])),
                ('name', models.CharField(max_length=100)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file', to='order.order')),
            ],
        ),
    ]
