# api/urls.py
from django.urls import path
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

# Initialize the Wagtail API router for write-enabled endpoints
api_router = WagtailAPIRouter('wagtailadmin')
# Register page, image, and document endpoints
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)

urlpatterns = [
    # Mount the API router directly at the root of this app
    path('', api_router.urls),
]
