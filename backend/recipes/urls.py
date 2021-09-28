from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecieptViewSet

router = DefaultRouter()
router.register(r'reciepts', RecieptViewSet, basename='reciepts')

urlpatterns = [
    path('v1/', include(router.urls)),
]