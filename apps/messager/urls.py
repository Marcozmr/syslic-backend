from django.urls import include, path
from rest_framework import routers

from .views import (
    MessageViewSet,
    MessageVisualizationViewSet,
)

app_name = 'message'

router = routers.DefaultRouter()
router.register(r'visualization', MessageVisualizationViewSet, basename="MessageVisualization")
router.register(r'', MessageViewSet, basename="Message")

urlpatterns = [
    path('', include(router.urls)),
]
