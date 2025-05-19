from email.policy import default
from itertools import product
from rest_framework import serializers
from apps.utils.fields import FileBase64Field
from drf_extra_fields.fields import Base64ImageField

from .models import (
    Image,
    Unity,
    Warranty,
    Classifier,
    Type,
    Product,
    Item,
    MaterialList,
    ProductFile,
)

from apps.supplier.serializers import (
    SupplierSerializer,
    SupplierBasicSerializer,
    SupplierNameSerializer,
)

class ImageProductSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        required=True,
        represent_in_base64=True,
        allow_null=True,
        allow_empty_file=True
    )
    class Meta:
        model = Image
        fields = ['id', 'image']
    
    def save(self, album=None, default=False):
        image_data = self.validated_data.get('image')
        image = Image.objects.create(album=album, default=default, image=image_data)
        image.save()

class AlbumProductSerializer(serializers.Serializer):
    image = ImageProductSerializer(many=True)

class UnitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Unity
        fields = ('id', 'unity', 'symbol')

class WarrantySerializer(serializers.ModelSerializer):
    class Meta:
        model = Warranty
        fields = ('id', 'name')

class ClassifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classifier
        fields = ('id', 'name')

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'name')

class ProductFileSerializer(serializers.ModelSerializer):
    file = FileBase64Field(
        required=True,
        represent_in_base64=True,
        allow_null=True,
        allow_empty_file=True
    )

    class Meta:
        model = ProductFile
        fields = ['id', 'file', 'file_name', 'product']

class ProductFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFile
        fields = [
            'id',
            'file_name',
        ]
        
class ProductSerializer(serializers.ModelSerializer):
    supplier_set = SupplierSerializer(source='supplier',
                                      read_only=True)

    warranty_set = WarrantySerializer(source='warranty',
                                      read_only=True)

    unity_set = UnitySerializer(source='unity',
                                read_only=True)

    classifier_set = ClassifierSerializer(source='classifier',
                                          read_only=True)

    type_set = ProductTypeSerializer(source='type',
                                     read_only=True)

    file_set = ProductFileDetailSerializer(source='file',
                                           read_only=True,
                                           many=True)
    
    class Meta:
        model = Product
        read_only_fields = (
            'get_price',
            'has_material_list',
        )
        fields = [
            'id',
            'name',
            'description',
            'brand',
            'model',
            'price',
            'anvisa',
            'code',
            'link_supplier',
            'supplier',
            'supplier_set',
            'warranty',
            'warranty_set',
            'unity',
            'unity_set',
            'classifier',
            'classifier_set',
            'type',
            'type_set',
            'file_set',
            'expiration_date',
            'weight',
            'lenght',
            'width',
            'height',
            'get_price',
            'has_material_list',
        ]

class ProductBasicSerializer(serializers.ModelSerializer):
    supplier_set = SupplierBasicSerializer(source='supplier',
                                           read_only=True)

    unity_set = UnitySerializer(source='unity',
                                read_only=True)

    class Meta:
        model = Product
        
        fields = [
            'id',
            'name',
            'description',
            'brand',
            'model',
            'price',
            'supplier',
            'supplier_set',
            'unity',
            'unity_set',
        ]

class ProductNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
        ]

class ProductToDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'width',
            'height',
            'lenght',
            'weight',
        ]

class ProductToAssistanceSerializer(serializers.ModelSerializer):
    supplier_set = SupplierNameSerializer(source='supplier',
                                             read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'brand',
            'model',
            'supplier',
            'supplier_set',
        ]

class ProductListSerializer(serializers.ModelSerializer):
    supplier_set = SupplierBasicSerializer(source='supplier',
                                          read_only=True)

    warranty_set = WarrantySerializer(source='warranty',
                                      read_only=True)

    unity_set = UnitySerializer(source='unity',
                                read_only=True)

    classifier_set = ClassifierSerializer(source='classifier',
                                          read_only=True)

    type_set = ProductTypeSerializer(source='type',
                                     read_only=True)
    
    class Meta:
        model = Product
        read_only_fields = (
            'get_price',
        )
        fields = [
            'id',
            'name',
            'description',
            'brand',
            'model',
            'price',
            'anvisa',
            'code',
            'link_supplier',
            'supplier',
            'supplier_set',
            'warranty',
            'warranty_set',
            'unity',
            'unity_set',
            'classifier',
            'classifier_set',
            'type',
            'type_set',
            'expiration_date',
            'weight',
            'lenght',
            'width',
            'height',
            'get_price',
        ]

class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Item
        fields = [
            'id',
            'product',
            'quantity'
        ]
        extra_kwargs = {
            'product': {'read_only': True, },
        }
        
class MaterialListSerializer(serializers.ModelSerializer):
    materials_set = ItemSerializer(many=True)
    item_root_set = ItemSerializer(source='item_root', read_only=True)
    class Meta:
        model = MaterialList
        fields = [
            'id',
            'name',
            'item_root',
            'item_root_set',
            'materials_set',
        ]
        depth = 2
