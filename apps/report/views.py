from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as django_filters

from .models import (
    Report,
)

from .serializers import (
    ReportSerializer,
)

from .pagination import (
    ReportPagination,
)

from .permissions import (
    IsAuthenticated,
)

class ReportViewSet(ModelViewSet):
    http_method_names = ['get', 'options', 'head']
    permission_classes = (IsAuthenticated,)
    serializer_class = ReportSerializer
    pagination_class = ReportPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'name',
        'module',
    ]

    ordering_fields = [
        'id',
        'name',
        'module',
        'default',
    ]

    ordering = ['name']

    filter_fields = {
        'id': ['exact'],
        'module': ['exact'],
        'name': ['exact'],
        'default': ['exact'],
    }

    def get_queryset(self):
        return Report.objects.all().order_by('pk')
