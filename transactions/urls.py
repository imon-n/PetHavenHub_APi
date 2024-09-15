from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet

router = DefaultRouter()
router.register('transactions', TransactionViewSet)  # Register with an empty prefix

urlpatterns = [
    path('', include(router.urls)),  # The base path will be 'transactions/'
]
