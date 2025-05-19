from django.urls import include, path
from rest_framework import routers

from .views import (
    HiringModalitieViewSet,
    SpheresViewSet,
    PowersViewSet,
    TypeCallingInstrumentViewSet,
    PncpFilterViewSet,
)

app_name = 'pncp'

router = routers.DefaultRouter()
router.register(r'hiring-modalitie', HiringModalitieViewSet, basename="PncpHiringModalitie")
router.register(r'spheres', SpheresViewSet, basename="PncpSpheres")
router.register(r'powers', PowersViewSet, basename="PncpPowers")
router.register(r'type-calling-instrument', TypeCallingInstrumentViewSet, basename="PncpTypeCallingInstrument")
router.register(r'filter', PncpFilterViewSet, basename="PncpFilter")

urlpatterns = [
    path('', include(router.urls)),
]
