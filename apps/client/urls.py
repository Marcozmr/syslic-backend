from django.urls import include, path
from rest_framework import routers


from .views import (
   ClientViewSet,
   ClientListViewSet,
)

app_name = 'client'

router = routers.DefaultRouter()
router.register(r'list', ClientListViewSet, basename="ClientList")
router.register(r'', ClientViewSet, basename="Client")

urlpatterns = [
    path('', include(router.urls)),
]
