from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from shopapp.sitemaps import ShopSitemap, StaticViewSitemap

schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version='v1',
        description="API для интернет-магазина",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

sitemaps = {
    'products': ShopSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += i18n_patterns(
    path('', lambda request: redirect('shopapp:index'), name='root'),
    path('shop/', include('shopapp.urls')),
    path('accounts/', include('myauth.urls')),
    path('blog/', include('blogapp.urls')),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)