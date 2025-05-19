

import apps.company.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_authentication', models.CharField(blank=True, max_length=100, null=True)),
                ('annotation', models.CharField(blank=True, max_length=100, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='certificate_client', to='client.client')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificate_company', to='company.company')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyCertificateStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyCertificateFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=apps.company.models.CompanyCertificateFile.upload_to_path, validators=[apps.company.models.CompanyCertificateFile.validate_file_size])),
                ('file_name', models.CharField(max_length=100)),
                ('certificate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificate_files', to='company.companycertificate')),
            ],
        ),
        migrations.AddField(
            model_name='companycertificate',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='certificate_status', to='company.companycertificatestatus'),
        ),
    ]
