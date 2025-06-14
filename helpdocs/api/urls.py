# helpdocs/api/urls.py
from helpdocs.api.views import HelpPageViewSet, HowToIndexViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

# your existing Wagtail headless API router:
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

api_router = WagtailAPIRouter('wagtailapi')
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)

# add a DRF router for HelpPage:

rest_router = DefaultRouter()
rest_router.register(r'help', HelpPageViewSet, basename='helpdocs')
rest_router.register(r'howto', HowToIndexViewSet, basename='howto')

urlpatterns = [
    # headless-Wagtail
    path('', include(rest_router.urls)),
    path('', api_router.urls),
]
