# project/urls.py

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from users.views import bridge_login_view


urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("bridge-login/", bridge_login_view, name='bridge-login'),
    path('approval/', include('approval.api.urls')),
    path("django-admin/", admin.site.urls),
    path("documents/", include(wagtaildocs_urls)),
    path("helpdocs/", include('helpdocs.api.urls')),
    path("search/", search_views.search, name="search"),
    path("users/", include('users.api.urls')),
]

# Serve static and media files in development only
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# Catch-all for Wagtail page routing — must go last
urlpatterns += [
    path("", include(wagtail_urls)),
]
