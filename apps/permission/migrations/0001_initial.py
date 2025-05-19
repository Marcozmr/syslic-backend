

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProfilePermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PermissionOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_option', models.CharField(choices=[('Default', 'Padrão'), ('User', 'Usuários'), ('Permission', 'Permissões'), ('Company', 'Empresas'), ('Client', 'Clientes'), ('Bidding', 'Licitações'), ('BiddingSettings', 'Configurações de Licitações'), ('Supplier', 'Fornecedores'), ('SupplierSettings', 'Configurações de Fornecedores'), ('Product', 'Produtos'), ('ProductSettings', 'Configurações de Produtos'), ('TransportSettings', 'Configurações de Transporte')], default='Default', max_length=50, verbose_name='Modulos')),
                ('permission_read', models.BooleanField(default=False, verbose_name='Visualizar')),
                ('permission_write', models.BooleanField(default=False, verbose_name='Criar')),
                ('permission_update', models.BooleanField(default=False, verbose_name='Atualizar')),
                ('permission_delete', models.BooleanField(default=False, verbose_name='Apagar')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='permission.profilepermissions')),
            ],
        ),
    ]
