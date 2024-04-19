"""scoretize_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.urls import re_path as url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from .views.CustomTokenRefreshView import CustomTokenRefreshView


schema_view = get_schema_view(
    openapi.Info(
        title="Scoretize API",
        default_version='V1',
        description="Scoretize Documentation",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('settings/', include('api.routers.settings')),
    path('project/', include('api.routers.project')),
    path('sector/', include('api.routers.sector')),
    path('user/', include('api.routers.user')),
    path('pitch/', include('api.routers.pitch')),
    path('overview/', include('api.routers.overview')),
    path('website/', include('api.routers.website')),
    path('seo/', include('api.routers.seo')),
    path('paid-media/', include('api.routers.searchAds')),
    path('socialMedia/', include('api.routers.socialMedia')),
    path('chron/', include('api.routers.chronTrigger')),
    path('global/', include('api.routers.globalv')),
    path('export/', include('api.routers.export')),
    path('performance/', include('api.routers.performance.performanceCalc')),
    path('performance/', include('api.routers.performance.performance')),
    path('account/', include('api.routers.account')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    url(r'^auth/', include('djoser.urls')),

    # Provided by simple JWT for token refresh logic
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(),
         name='token_refresh'),
]
