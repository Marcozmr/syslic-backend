from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="SysLic API",
        default_version='v1',
        description="SysLic API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contato@coorlab.com.br"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

system_url = [
    path('admin/', admin.site.urls),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger',
        cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc',
        cache_timeout=0), name='schema-redoc'),
]

apps_url = [
    path('silk/', include('silk.urls', namespace='silk')),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/permission/', include('apps.permission.urls')),
    path('api/v1/address/', include('apps.address.urls')),
    path('api/v1/company/', include('apps.company.urls')),
    path('api/v1/client/', include('apps.client.urls')),
    path('api/v1/bidding/', include('apps.bidding.urls')),
    path('api/v1/supplier/', include('apps.supplier.urls')),
    path('api/v1/product/', include('apps.product.urls')),
    path('api/v1/transport/', include('apps.transport.urls')),
    path('api/v1/contact/', include('apps.contact.urls')),
    path('api/v1/order/', include('apps.order.urls')),
    path('api/v1/messager/', include('apps.messager.urls')),
    path('api/v1/contract/', include('apps.contract.urls')),
    path('api/v1/pncp/', include('apps.pncp.urls')),
    path('api/v1/commission/', include('apps.commission.urls')),
    path('api/v1/metadata/', include('apps.metadata.urls')),
    path('api/v1/report/', include('apps.report.urls')),
]

urlpatterns = system_url + apps_url + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
