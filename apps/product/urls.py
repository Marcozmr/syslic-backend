from django.urls import include, path
from rest_framework import routers

from .views import (
    WarrantyViewSet,
    UnityViewSet,
    ClassifiersViewSet,
    TypeViewSet,
    ProductViewSet,
    MaterialListViewSet,
    ItemMaterialListViewSet,
    MaterialListView,
    AlbumProductViewSet,
    ImageProductViewSet,
    ProductFileViewSet,
    ProductImportViewSet,
    ProductValidateViewSet,
    ProductListViewSet,
)

app_name = 'product'

router = routers.SimpleRouter()
router.register(r'warranty', WarrantyViewSet, basename="product-warranty")
router.register(r'unity', UnityViewSet, basename="product-unity")
router.register(r'classifiers', ClassifiersViewSet, basename="product-classifiers")
router.register(r'type', TypeViewSet, basename="product-type")
router.register(r'material-list', MaterialListViewSet, basename="material-list")
router.register(r'material-list/item', ItemMaterialListViewSet, basename="item")
router.register(r'imagem', ImageProductViewSet, basename="imagem")
router.register(r'attach/file', ProductFileViewSet, basename="ProductFile")
router.register(r'list', ProductListViewSet, basename="product-list")
router.register(r'', ProductViewSet, basename="product")

urlpatterns = [
    path('', include(router.urls)),
    path(r'<int:pk>/material-list/', MaterialListView.as_view()),
    path(r'<int:pk>/album/', AlbumProductViewSet.as_view({
        'get': 'list',
        'post': 'set_image',
    })),
    path(r'<int:pk>/default_image/', AlbumProductViewSet.as_view({
        'get': 'default_image',
    })),
    path(r'validate/file/', ProductValidateViewSet.as_view({
        'post': 'validate_csv',
    })),
    path(r'import/file/', ProductImportViewSet.as_view({
        'post': 'import_products',
    }))
]
