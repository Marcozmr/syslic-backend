

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('module', models.CharField(max_length=255)),
                ('thread', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=5000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='messages', to='accounts.profile')),
                ('mentions', models.ManyToManyField(blank=True, related_name='mentions', to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='MessageVisualization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='viewers', to='messager.message')),
                ('viewer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.profile')),
            ],
        ),
    ]
