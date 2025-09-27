from django.contrib import admin
from django.urls import path, include, re_path

# Import Swagger dependencies
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# 1. Define the Schema View
schema_view = get_schema_view(
   openapi.Info(
      title="ALX Travel App API",
      default_version='v1',
      description="API documentation for the ALX Travel App",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@alx.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # 2. Swagger/Redoc URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API Routes
    path('api/', include('listings.urls')), # Assuming you will create this file
]