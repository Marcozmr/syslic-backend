import uuid
from PIL import Image as ImagePIL
from django.db.models.signals import post_save
from django.db.models import UniqueConstraint

from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_delete, pre_save, post_save
from django.db.models.fields.related import ForeignKey
from django.core.exceptions import ValidationError
from treebeard.exceptions import InvalidPosition
from treebeard.mp_tree import MP_Node

from django_multitenant.models import TenantModel
from django_multitenant.mixins import TenantModelMixin
from django_multitenant.fields import TenantForeignKey

from apps.supplier.models import (
    Supplier,
)

from apps.accounts.models import (
    Account,
    AccountTenantManager,
)

class ImageAlbum(models.Model):
    def default(self):
        try:
            image = self.images.all().get(default=True)
        except Image.DoesNotExist:
            image = None
        return image

class Image(TenantModel):
    def validate_image_size(field_file):
        file_size = field_file.file.size
        megabyte_limit = 15.0
        if file_size > megabyte_limit*1024*1024:
            raise ValidationError('Max file size is 15MB')

    def get_upload_path(instance, filename):
        model = instance.album.model.__class__._meta
        model_name = model.verbose_name_plural.replace(' ', '_')
        item_name = instance.album.model.name.replace(' ', '_').lower()
        return f'album/{model_name}/images/{item_name}/{filename}'

    image = models.ImageField('Image',
                              blank=False,
                              upload_to=get_upload_path,
                              validators=[validate_image_size])

    album = models.ForeignKey(ImageAlbum,
                             related_name='images',
                             on_delete=models.CASCADE)

    default = models.BooleanField(default=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='ProductImage')

    class Meta:
        unique_together = (
            'id',
            'account',
        )

    class TenantMeta:
        tenant_field_name = "account_id"

def image_compressor(sender, **kwargs): 
    if kwargs["created"]:
        with ImagePIL.open(kwargs["instance"].image.path) as photo:
            photo.save(kwargs["instance"].image.path, optimize=True, quality=20)

post_save.connect(image_compressor, sender=Image)

class Unity(TenantModel):
    objects = AccountTenantManager()

    unity = models.CharField(max_length=200,
                             blank=False,
                             null=False)

    symbol = models.CharField(max_length=200,
                              blank=False,
                              null=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='ProductUnity')

    class Meta:
        unique_together = (
            'id',
            'account',
        )
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_unity_id_account'),
            UniqueConstraint(fields=['unity', 'account'], name='unique_unity_unity_account'),
            UniqueConstraint(fields=['symbol', 'account'], name='unique_unity_symbol_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"
    
class Warranty(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=200,
                            blank=False,
                            null=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='ProductWarranty')

    class Meta:
        unique_together = (
            'id',
            'account',
        )
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_warranty_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_warranty_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class Classifier(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=200,
                            blank=False,
                            null=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='ProductClassifier')

    class Meta:
        unique_together = (
            'id',
            'account',
        )
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_classifier_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_classifier_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class Type(TenantModel):
    objects = AccountTenantManager()

    name = models.CharField(max_length=200,
                            blank=False,
                            null=False)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='ProductType')

    class Meta:
        unique_together = (
            'id',
            'account',
        )
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_type_id_account'),
            UniqueConstraint(fields=['name', 'account'], name='unique_type_name_account'),
        ]

    class TenantMeta:
        tenant_field_name = "account_id"

class Product(TenantModel):
    name = models.TextField(null=False,
                            blank=False)

    description = models.TextField(null=True,
                                   blank=True)

    brand = models.TextField(null=True,
                             blank=True)

    model = models.TextField(null=True,
                             blank=True)

    price = models.DecimalField(decimal_places=2,
                                max_digits=20,
                                default=0.01,
                                null=False,
                                blank=False)

    anvisa = models.CharField(max_length=200,
                              null=True,
                              blank=True)

    code = models.CharField(max_length=200,
                            null=True,
                            blank=True)

    link_supplier = models.TextField(null=True,
                                     blank=True)

    supplier = TenantForeignKey(Supplier,
                                 on_delete=models.PROTECT,
                                 null=True,
                                 blank=True)

    warranty = TenantForeignKey(Warranty,
                                 on_delete=models.PROTECT,
                                 null=True,
                                 blank=True)

    unity = TenantForeignKey(Unity,
                              on_delete=models.PROTECT,
                              null=True,
                              blank=True)

    classifier = TenantForeignKey(Classifier, 
                                  on_delete=models.PROTECT,
                                  null=True,
                                  blank=True)

    type = TenantForeignKey(Type, 
                             on_delete=models.PROTECT,
                             null=True,
                             blank=True)

    expiration_date = models.DateField(null=True,
                                       blank=True)

    weight = models.DecimalField(decimal_places=3,
                                 max_digits=20,
                                 null=True,
                                 blank=True)

    lenght = models.DecimalField(decimal_places=2,
                                 max_digits=20,
                                 null=True,
                                 blank=True)

    width = models.DecimalField(decimal_places=2,
                                max_digits=20,
                                null=True,
                                blank=True)

    height = models.DecimalField(decimal_places=2,
                                 max_digits=20,
                                 null=True,
                                 blank=True)

    album = models.OneToOneField(ImageAlbum,
                                 related_name='model',
                                 on_delete=models.PROTECT,
                                 blank=True,
                                 null=True)

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='Product')

    class Meta:
        unique_together = (
            'id',
            'account',
        )
        constraints = [
            UniqueConstraint(fields=['id', 'account'], name='unique_product_id_account'),
            UniqueConstraint(fields=['model', 'account'], name='unique_product_model_account'),
        ]


    class TenantMeta:
        tenant_field_name = "account_id"

    def get_price(self):
        list_itens = Item.objects.filter(product=self)
        list_materials = []
        for item in list_itens:
            if item.is_root():
                list_materials = MaterialList.objects.filter(item_root=item)
                if list_materials:
                    return list_materials[0].get_price()
        return self.price

    def has_material_list(self):
        list_itens = Item.objects.filter(product=self)
        for item in list_itens:
            if item.is_root():
                if MaterialList.objects.filter(item_root=item).exists():
                    return True
        return False

class Item(MP_Node):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    def get_who_depends_on_me(self, level=0, root=None):
        items = Item.objects.filter(product=self.product)
        qs = Item.objects.none()
        rootItem = root

        if root is None:
            rootItem = self

        for item in items:
            ancestors = item.get_ancestors()

            if ancestors:
                for ancestor in ancestors:
                    valid_material_list = ancestor.material_list
                    if valid_material_list:
                        if (item.product != rootItem.product):
                            qs = qs.union(Item.objects.filter(id=item.id))
                        qs = qs.union(Item.objects.filter(id=ancestor.id))
                        qs = qs.union(ancestor.get_who_depends_on_me(level=(level+1), root=rootItem))
                
        return qs

    def get_who_i_depend_on(self, level=0):
        items = Item.objects.filter(product=self.product)
        qs = Item.objects.none()

        if level:
            qs = qs.union(items)

        for item in items:
            decendants = item.get_descendants()

            if decendants:
                qs = qs.union(decendants)
                for decendant in decendants:
                    qs = qs.union(decendant.get_who_i_depend_on((level+1)))
                
        return qs

    def is_circular_dependency(self, product):
        is_true = False
        parents = self.get_who_depends_on_me()

        for parent in parents:
            if parent.product == product:
                 is_true = True

        return is_true

class MaterialList(TenantModel):
    name = models.CharField(max_length=200)

    item_root = models.ForeignKey(Item,
                                  on_delete=models.CASCADE,
                                  related_name='material_list')

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='ProductMaterialList')

    class Meta:
        unique_together = (
            'id',
            'account',
        )

    class TenantMeta:
        tenant_field_name = "account_id"

    def materials_set(self):
        return self.item_root.get_descendants()

    def get_price(self):
        item_list = self.item_root.get_children()
        value = 0
        for item in item_list:
            value += (item.quantity * item.product.get_price())
        return value
    
class ProductFile(TenantModel):
    def validate_file_size(field_file):
        file_size = field_file.file.size
        megabyte_limit = 15.0
        if file_size > megabyte_limit*1024*1024:
            raise ValidationError('Max file size is 15MB')


    def upload_to_path(self, filename):
        ext = filename.split('.')[-1]
        name = uuid.uuid4().hex
        return 'product/{}.{}'.format(name, ext)

    file = models.FileField(upload_to=upload_to_path,
                           blank=True,
                           null=True,
                           validators=[validate_file_size])

    file_name = models.TextField(blank=False,
                                null=False)

    product = TenantForeignKey(Product,
                              on_delete=models.CASCADE,
                              blank=False,
                              null=False,
                              related_name="file")

    account = models.ForeignKey(Account,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='ProductFile')

    class Meta:
        unique_together = (
            'id',
            'account',
        )

    class TenantMeta:
        tenant_field_name = "account_id"

@receiver(post_save, sender=Product)
def create_product_album(sender, instance=None, **kwargs):
    if instance.album is None:
        album = ImageAlbum.objects.create()
        instance.album = album
        instance.save()

@receiver(post_delete, sender=MaterialList)
def delete_material_item_root(sender, instance=None, **kwargs):
    if instance:
        instance.item_root.delete()

@receiver(pre_save, sender=Item)
def create_product_node(sender, instance=None, **kwargs):
    if instance.is_leaf():
        root = instance.get_parent()
        if root is not None:
            if instance.product.id == root.product.id:
                raise ValidationError('The material list must not contain your own product')
            if root.is_circular_dependency(instance.product):
                raise ValidationError('Invalid operation, a circular dependency was detected')
