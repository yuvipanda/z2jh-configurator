from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(
        "services/configurator/",
        include(
            [

                # configurator is the default app, so let's put it under /
                path("", include("z2jh_configurator.configurator.urls")),
                path("admin/", admin.site.urls),
                path("", include("social_django.urls", namespace="social")),
            ]
        ),
    )
]
