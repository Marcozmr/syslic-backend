from django.urls import include, path
from rest_framework import routers

from .views import (
   ContactViewSet,
)

app_name = 'contact'

router = routers.DefaultRouter()
router.register(r'', ContactViewSet, basename="Contact")

urlpatterns = [
    path('', include(router.urls)),
]
