from import_export.admin import ImportExportMixin
from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import (
    Image,
    ImageAlbum,
    Unity,
    Warranty,
    Classifier,
    Type,
    Product,
    Item,
    MaterialList,
    ProductFile,
)

class ImageAdmin(ImportExportMixin, admin.StackedInline):
    model = Image

class ImageAlbumAdmin(ImportExportMixin, admin.ModelAdmin):
    inlines = [ImageAdmin]

    class Meta:
        model = ImageAlbum

class UnityAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['unity', 'symbol']

class WarrantyAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'name']

class ClassifierAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'name']

class TypeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'name']
    
class ProductAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name', 'description', 'code', 'classifier', 'type']

class ProductFileAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['file', 'file_name', 'product']
    
class ItemAdmin(ImportExportMixin, TreeAdmin):
    form = movenodeform_factory(Item)

class MaterialListAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name']

admin.site.register(ImageAlbum)
admin.site.register(Image)
admin.site.register(Unity, UnityAdmin)
admin.site.register(Warranty, WarrantyAdmin)
admin.site.register(Classifier, ClassifierAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductFile, ProductFileAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(MaterialList, MaterialListAdmin)
