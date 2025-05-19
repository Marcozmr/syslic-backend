

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_alter_company_complement'),
        ('bidding', '0015_auto_20231026_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='BiddingCompanyFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidding', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bidding.bidding')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company.companyfile')),
            ],
        ),
        migrations.CreateModel(
            name='BiddingCompanyCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidding', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bidding.bidding')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company.companycertificate')),
            ],
        ),
    ]
