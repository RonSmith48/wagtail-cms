from rest_framework.routers import DefaultRouter
from django.urls import path, include
from approval.api.views import BusinessDocumentViewSet

router = DefaultRouter()
router.register(r'documents', BusinessDocumentViewSet,
                basename='business-docs')

urlpatterns = [
    path('', include(router.urls)),
]
