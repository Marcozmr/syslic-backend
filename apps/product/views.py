
import csv
from datetime import datetime
from rest_framework import filters, serializers
from django_filters import rest_framework as django_filters
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.db import (
    transaction,
    IntegrityError,
)
from django.http import Http404
from django.core.exceptions import ValidationError

from apps.utils.cache import ModelViewSetCached

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

from apps.supplier.models import (
    Supplier,
)

from .serializers import (
    ImageProductSerializer,
    AlbumProductSerializer,
    UnitySerializer,
    WarrantySerializer,
    ClassifierSerializer,
    ProductTypeSerializer,
    ProductSerializer,
    ItemSerializer,
    MaterialListSerializer,
    ProductFileSerializer,
    ProductListSerializer,
)

from .permissions import (
        HasModelPermission,
        HasOtherPermission,
        HasProductSettingsPermission
)

from .pagination import ProductPagination

class WarrantyViewSet(ModelViewSetCached):
    permission_classes = (HasProductSettingsPermission | HasOtherPermission,)
    serializer_class = WarrantySerializer
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

    def get_queryset(self):
        return Warranty.objects.all().order_by('pk')

class UnityViewSet(ModelViewSetCached):
    permission_classes = (HasProductSettingsPermission | HasOtherPermission,)
    serializer_class = UnitySerializer
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'unity',
        'symbol',
        ]

    def get_queryset(self):
        return Unity.objects.all().order_by('pk')

class ClassifiersViewSet(ModelViewSetCached):
    permission_classes = (HasProductSettingsPermission | HasOtherPermission,)
    serializer_class = ClassifierSerializer
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

    def get_queryset(self):
        return Classifier.objects.all().order_by('pk')

class TypeViewSet(ModelViewSetCached):
    permission_classes = (HasProductSettingsPermission | HasOtherPermission,)
    serializer_class = ProductTypeSerializer
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

    def get_queryset(self):
        return Type.objects.all().order_by('pk')

class ProductViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'name',
        'description',
        'brand',
        'model',
        'price',
        'anvisa',
        'code',
        'link_supplier',
        'supplier__name',
        'supplier__name_fantasy',
        'warranty__name',
        'unity__symbol',
        'unity__unity',
        'classifier__name',
        'type__name',
        'expiration_date',
        ]

    ordering_fields = [
        'id',
        'name',
        'description',
        'brand',
        'model',
        'price',
        'anvisa',
        'code',
        'link_supplier',
        'supplier__name',
        'warranty__name',
        'unity__symbol',
        'unity__unity',
        'classifier__name',
        'type__name',
        'expiration_date',
        ]

    filter_fields = {
            'id': ['exact'],
        }

    def get_queryset(self):
        id_list = self.request.GET.getlist('id[]')

        if id_list:
            return Product.objects.filter(id__in=id_list).order_by('pk')
        else:
            return Product.objects.all().order_by('pk')

class ProductListViewSet(ModelViewSetCached):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'name',
        'description',
        'brand',
        'model',
        'price',
        'anvisa',
        'code',
        'link_supplier',
        'supplier__name',
        'supplier__name_fantasy',
        'warranty__name',
        'unity__symbol',
        'unity__unity',
        'classifier__name',
        'type__name',
        'expiration_date',
        ]

    ordering_fields = [
        'id',
        'name',
        'description',
        'brand',
        'model',
        'price',
        'anvisa',
        'code',
        'link_supplier',
        'supplier__name',
        'warranty__name',
        'unity__symbol',
        'unity__unity',
        'classifier__name',
        'type__name',
        'expiration_date',
        ]

    filter_fields = {
            'id': ['exact'],
        }

    def get_queryset(self):
        id_list = self.request.GET.getlist('id[]')

        if id_list:
            return Product.objects.filter(id__in=id_list).order_by('pk')
        else:
            return Product.objects.select_related('supplier',
                                                  'warranty',
                                                  'unity',
                                                  'classifier',
                                                  'type',).order_by('pk')

class MaterialListViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = MaterialListSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        return MaterialList.objects.all().order_by('pk')

    def set_items(item_root, product, quantity):
        pass

    def create(self, request, *args, **kwargs):
        data = request.data
        product = Product.objects.get(id=data["product"])
        item_root = Item.add_root(product=product, quantity=1)
        material_list = MaterialList.objects.create(name=data["name"],
                                                    item_root=item_root)

        if len(data["materials_set"]) <= 0:
            response = {
                    'status': 'error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'The list cannot be empty.',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        for item in data["materials_set"]:
            product = Product.objects.get(id=item["product"]["id"])
            quantity = item["quantity"]
            item = Item(product=product, quantity=quantity)

            try:
                item_root.add_child(instance=item)
            except ValidationError as error:
                response = {
                        'status': 'error',
                        'code': status.HTTP_400_BAD_REQUEST,
                        'message': error.message,
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        material_list.save()
        serializer = MaterialListSerializer(material_list)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = request.data
        material_list = self.get_object()
        material_list.name = data.get('name', material_list.name)

        if len(data["materials_set"]) <= 0:
            response = {
                    'status': 'error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'The list cannot be empty.',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        item_root = material_list.item_root

        for item in data["materials_set"]:
            quantity = item["quantity"]
            item_id = item.get('id', None)
            if item_id != None:
                update_item = Item.objects.get(id=item["id"])
                update_item.quantity = quantity
                update_item.save()
            else:
                product = Product.objects.get(id=item["product"]["id"])
                item = Item(product=product, quantity=quantity)

                try:
                    item_root.add_child(instance=item)
                except ValidationError as error:
                    response = {
                            'status': 'error',
                            'code': status.HTTP_400_BAD_REQUEST,
                            'message': error.message,
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)

        material_list.save()
        serializer = MaterialListSerializer(material_list)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def has_active_list(self):
        material_list = self.get_object()
        product = material_list.item_root.product
        is_true = MaterialList.objects.filter(item_root__product=product).exists()
        return is_true

class ItemMaterialListViewSet(ModelViewSetCached):
    http_method_names = ['head', 'options', 'delete',]
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.all().order_by('pk')

class MaterialListView(ListAPIView):
    serializer_class = MaterialListSerializer
    permission_classes = (HasModelPermission | HasOtherPermission,)
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

    def get_queryset(self):
        if 'pk' in self.kwargs:
            id = self.kwargs['pk']
            product = Product.objects.get(id=id)
            return MaterialList.objects.filter(item_root__product=product)
        else:
            return MaterialList.objects.none()

class AlbumProductViewSet(ModelViewSet):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ImageProductSerializer

    def get_queryset(self):
        if 'pk' in self.kwargs:
            id = self.kwargs['pk']
            product = Product.objects.get(id=id)
            album = product.album
            return album.images.all()
        else:
            return ImageAlbum.objects.none()

    def get_object(self, id):
        try:
            product = Product.objects.get(id=id)
            return product.album
        except ImageAlbum.DoesNotExist:
            raise Http404

    @action(detail=True, methods=['get'])
    def default_image(self, request, pk=None):
        id = self.kwargs['pk']
        album = self.get_object(id)
        serializer = ImageProductSerializer(album.default())
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def set_image(self, request, pk=None):
        id = self.kwargs['pk']
        album = self.get_object(id)
        serializer = ImageProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(album=album)
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Product image add successfully',
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageProductViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ImageProductSerializer

    def get_queryset(self):
        return Image.objects.all()

class ProductFileViewSet(ModelViewSetCached):
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ProductFileSerializer

    def get_queryset(self):
        return ProductFile.objects.all().order_by('pk')

def validate_csv_models(file):
    decoded_file = file.read().decode('utf-8').splitlines()
    reader = csv.reader(decoded_file)
    keys = next(reader)
    models = []

    invalid_string = 'INVALID VALUE'
    invalid_id = -1

    attributes_relation = {
            "id": "id",
            "Nome": "name",
            "Descrição": "description",
            "Marca": "brand",
            "Modelo": "model",
            "Preço": "price",
            "Nº Anvisa": "anvisa",
            "Código": "code",
            "Link do fornecedor": "link_supplier",
            "CNPJ Fornecedor": "supplier",
            "Garantia": "warranty",
            "Unidade": "unity",
            "Categoria": "classifier",
            "Tipo": "type",
            "Data de validade": "expiration_date",
            "Peso": "weight",
            "Profundidade": "lenght",
            "Largura": "width",
            "Altura": "height"
        }

    for i in range(len(keys)):
        if keys[i] in attributes_relation:
            keys[i] = attributes_relation[keys[i]]

    for row in reader:
        data = dict(zip(keys, row))

        decimal_fields = ['weight', 'lenght', 'width', 'height']

        for field in decimal_fields:
            if data[field] != "":
                data[field] = data[field].replace(",", ".")

        if data["price"] != "":
            if ',' in data["price"]:
                data["price"] = data["price"].replace('.', '')
                data["price"] = data["price"].replace(",", ".")

        if data["expiration_date"] != "":
            initital_date = datetime.strptime(data["expiration_date"], "%d/%m/%Y")
            formated_date = initital_date.strftime("%Y-%m-%d")
            data["expiration_date"] = formated_date

        if data["supplier"] != "":
            try:
                supplier = Supplier.objects.get(cnpj__contains=data["supplier"])
                data["supplier"] = supplier.id
            except Supplier.DoesNotExist:
                data["supplier"] = invalid_id

        if data["warranty"] != "":
            try:
                warranty = Warranty.objects.get(name__iexact=data["warranty"])
                data["warranty"] = warranty.id
            except Warranty.DoesNotExist:
                data["warranty"] = invalid_id

        if data["unity"] != "":
            try:
                unity = Unity.objects.get(symbol__exact=data["unity"])
                data["unity"] = unity.id
            except Unity.DoesNotExist:
                data["unity"] = invalid_id

        if data["classifier"] != "":
            try:
                classifier = Classifier.objects.get(name__iexact=data["classifier"])
                data["classifier"] = classifier.id
            except Classifier.DoesNotExist:
                data["classifier"] = invalid_id

        if data["type"] != "":
            try:
                type = Type.objects.get(name__iexact=data["type"])
                data["type"] = type.id
            except Type.DoesNotExist:
                data["type"] = invalid_id

        filtered_data = {key: value for key, value in data.items() if value}

        models.append(filtered_data)

    return models

class ProductValidateViewSet(ModelViewSet):
    http_method_names = ['post', 'head', 'options']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'])
    def validate_csv(self, request, pk=None):
        res = {
            "valid": True,
            "errors": {},
        }

        file = request.FILES.get('file')

        if not file:
            return Response(
                {'error': 'No file found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = validate_csv_models(file)
        product_models = []

        for i in range(len(data)):
            data_id = data[i].get('id', None)

            if data_id is not None:
                product_instance = Product.objects.filter(id=data_id)

                if not product_instance.exists():
                    res['valid'] = False
                    res['errors'][f'Line {i+2}'] = {'id': ['invalid id to update.']}
                    continue

            float_fields = ['price', 'weight', 'lenght', 'width', 'height']

            for field in float_fields:
                field_value = data[i].get(field, None)

                if field_value is not None:
                    try:
                        data[i][field] = float(data[i][field])
                    except ValueError:
                        res['valid'] = False
                        res['errors'][f'Line {i+2}'] = {field: [f'invalid value for {field}.']}
                        continue

            if 'id' in data[i]:
                product_id = data[i]['id']
                product_instance = Product.objects.get(pk=product_id)
                serializer = ProductSerializer(product_instance, data=data[i])
            else:
                serializer = ProductSerializer(data=data[i])

            if serializer.is_valid():
                product_model = serializer.validated_data.get('model', None)

                if product_model is not None:
                    product_model = product_model.lower()

                    if product_model in product_models:
                        res['valid'] = False
                        res['errors'][f'Line {i+2}'] = {'model': ['product with this model already exists.']}
                        continue
                    else:
                        product_models.append(product_model)

            else:
                res['valid'] = False
                res['errors'][f'Line {i+2}'] = serializer.errors

        return Response(
            {'message': res},
            status=status.HTTP_200_OK
        )

class ProductImportViewSet(ModelViewSet):
    http_method_names = ['post', 'head', 'options']
    permission_classes = (HasModelPermission | HasOtherPermission,)
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'])
    def import_products(self, request, pk=None):
        file = request.FILES.get('file')

        if not file:
            return Response(
                {'error': 'No file found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = validate_csv_models(file)

        try:
            with transaction.atomic():
                for model_data in data:
                    product_id = model_data.get('id')

                    model_data
                    if product_id:
                        product_instance = Product.objects.get(pk=product_id)
                        serializer = ProductSerializer(product_instance, data=model_data)
                    else:
                        serializer = ProductSerializer(data=model_data)

                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise serializers.ValidationError(serializer.errors)

        except (IntegrityError, ValidationError) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'message': 'Products imported successfully'},
            status=status.HTTP_200_OK
        )
