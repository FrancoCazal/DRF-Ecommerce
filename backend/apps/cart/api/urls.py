from django.urls import path
from apps.cart.api.views import (
    CartView,
    CartAddView,
    CartUpdateView,
    CartRemoveView,
    CartClearView,
)

urlpatterns = [
    path('', CartView.as_view(), name='cart-detail'),
    path('add/', CartAddView.as_view(), name='cart-add'),
    path('update/<int:product_id>/', CartUpdateView.as_view(), name='cart-update'),
    path('remove/<int:product_id>/', CartRemoveView.as_view(), name='cart-remove'),
    path('clear/', CartClearView.as_view(), name='cart-clear'),
]
