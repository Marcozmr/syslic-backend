

import apps.product.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('quantity', models.PositiveIntegerField(default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unity', models.CharField(max_length=200, unique=True)),
                ('symbol', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Warranty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('brand', models.CharField(blank=True, max_length=200, null=True)),
                ('model', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.01, max_digits=20)),
                ('anvisa', models.CharField(blank=True, max_length=200, null=True)),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('link_supplier', models.CharField(blank=True, max_length=1000, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('lenght', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('width', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('album', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='model', to='product.imagealbum')),
                ('classifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.classifier')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='supplier.supplier')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.type')),
                ('unity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.unity')),
                ('warranty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.warranty')),
            ],
            options={
                'unique_together': {('name', 'description', 'brand', 'model', 'code')},
            },
        ),
        migrations.CreateModel(
            name='MaterialList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('item_root', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_list', to='product.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=apps.product.models.Image.get_upload_path, validators=[apps.product.models.Image.validate_image_size], verbose_name='Image')),
                ('default', models.BooleanField(default=False)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.imagealbum')),
            ],
        ),
    ]
