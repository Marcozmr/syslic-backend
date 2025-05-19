from django.urls import include, path
from rest_framework import routers

from .views import (
    ReportViewSet,
)

app_name = 'report'

router = routers.DefaultRouter()
router.register(r'', ReportViewSet, basename="Report")

urlpatterns = [
    path('', include(router.urls)),
]
