from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as django_filters

from .models import (
    Message,
    MessageVisualization,
)

from .serializers import (
    MessageSerializer,
    MessageVisualizationSerializer,
)

from .pagination import (
    MessagerPagination,
)

from .permissions import (
    HasModelPermission,
)

class MessageViewFilter(django_filters.FilterSet):
    not_viewed_by = django_filters.NumberFilter(
       field_name='viewers__viewer__id',
       exclude=True,
    )

    not_author = django_filters.NumberFilter(
       field_name='author__id',
       exclude=True,
    )

    create_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Message
        fields = {
          'id': ['exact'],
          'module': ['exact'],
          'thread': ['exact'],
          'mentions__id': ['exact'],
          'author__id': ['exact'],
          'viewers__viewer__id': ['exact'],
          'created_at': ['lte', 'gte', 'exact'],

        }

class MessageViewSet(ModelViewSet):
    permission_classes = (HasModelPermission,)
    serializer_class = MessageSerializer
    pagination_class = MessagerPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'module',
        'thread',
        'message',
        'created_at',
    ]

    ordering_fields = [
        'id',
        'module',
        'thread',
        'message',
        'created_at',
    ]

    ordering = ['created_at']

    filterset_class = MessageViewFilter

    def get_queryset(self):
        return Message.objects.all().order_by('pk')

class MessageVisualizationViewSet(ModelViewSet):
    permission_classes = (HasModelPermission,)
    serializer_class = MessageVisualizationSerializer
    pagination_class = MessagerPagination
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.DjangoFilterBackend]
    search_fields = [
        'id',
        'viewer',
        'message',
        'date',
    ]

    ordering_fields = [
        'id',
        'viewer',
        'message',
        'date',
    ]

    ordering = ['date']

    filter_fields = {
        'id': ['exact'],
        'viewer': ['exact'],
        'message': ['exact'],
        'date': ['lte', 'gte', 'exact'],
    }

    def get_queryset(self):
        return MessageVisualization.objects.all().order_by('pk')
