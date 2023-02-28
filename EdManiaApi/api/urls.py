from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg.generators import OpenAPISchemaGenerator


class CustomApiSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        swagger = super().get_schema(request, public)
        swagger.tags = [
            {"name": "Users", "description": "Handles user Creation & Authentications"},
            {
                "name": "Activities",
                "description": "Handles save user's children, activities and daily records",
            },
            {
                "name": "Reports",
                "description": "Retrieves a list of reports. Reports can be filtered by date range and report type",
            },
        ]
        return swagger


admin.site.ste_header = "EdMania Application Backend"
admin.site.index_title = "Backend"

schema_view = get_schema_view(
    openapi.Info(
        title="EdMania data source and API's",
        default_version="v1.0",
        description="APIs Doc",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="amosk7793@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=CustomApiSchemaGenerator,
)

admin.site.site_header = "Ed Mania Backend & Database"

urlpatterns = [
    path("admin/", admin.site.urls),
    # Open Api docs
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Application urls
    path("api/", include("application.urls")),
]
