from django.urls import include, path
from rest_framework import routers

from .views import (
   MetaDataViewSet,
)

app_name = 'metadata'

router = routers.DefaultRouter()
router.register(r'', MetaDataViewSet, basename="MetaData")

urlpatterns = [
    path('', include(router.urls)),
]
