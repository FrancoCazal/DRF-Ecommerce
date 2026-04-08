from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.products.api.views import CategoryListView, ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('', include(router.urls)),
]
