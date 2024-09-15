from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PetModelViewSet, CategoryModelViewSet, PurchaseHistoryViewSet

router = DefaultRouter()
router.register('pets', PetModelViewSet)
router.register('categories', CategoryModelViewSet)
router.register('purchase-history', PurchaseHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
