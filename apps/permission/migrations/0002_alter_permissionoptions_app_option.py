

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissionoptions',
            name='app_option',
            field=models.CharField(choices=[('Default', 'Padrão'), ('User', 'Usuários'), ('Permission', 'Permissões'), ('Company', 'Empresas'), ('Client', 'Clientes'), ('Bidding', 'Licitações'), ('BiddingSettings', 'Configurações de Licitações'), ('Supplier', 'Fornecedores'), ('SupplierSettings', 'Configurações de Fornecedores'), ('Product', 'Produtos'), ('ProductSettings', 'Configurações de Produtos'), ('TransportSettings', 'Configurações de Transporte'), ('Order', 'Pedidos'), ('OrderSettings', 'Configurações de Pedidos')], default='Default', max_length=50, verbose_name='Modulos'),
        ),
    ]
