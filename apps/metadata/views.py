from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from django_filters import rest_framework as django_filters

from .models import (
    MetaData,
)

from .serializers import (
    MetaDataSerializer,
)

from .pagination import (
    MetaDataPagination,
)

from .permissions import (
    IsAuthenticated,
)

class MetaDataViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MetaDataSerializer
    pagination_class = MetaDataPagination
    filter_backends = [django_filters.DjangoFilterBackend]
    http_method_names = ['get', 'post']

    filter_fields = {
        'id': ['exact'],
        'profile': ['exact'],
        'tag': ['exact'],
    }

    def get_queryset(self):
        return MetaData.objects.all().order_by('pk')
