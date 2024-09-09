from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lote_suinos.core.interfaces.views import LoteViewSet

router = DefaultRouter()
router.register(r'lotes', LoteViewSet, basename='lote')

urlpatterns = [
    path('', include(router.urls)),
]