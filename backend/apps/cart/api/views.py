from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.cart.services import CartService
from apps.cart.api.serializers import (
    AddToCartSerializer,
    CartDetailSerializer,
    UpdateCartItemSerializer,
)
from apps.products.models import Product


class CartView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cart = CartService(request.user)
        data = cart.get_cart_detail()
        serializer = CartDetailSerializer(data)
        return Response(serializer.data)


class CartAddView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        if not Product.objects.filter(id=product_id, is_active=True).exists():
            return Response(
                {'detail': 'Product not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart = CartService(request.user)
        new_qty = cart.add(product_id, quantity)
        return Response({'product_id': product_id, 'quantity': new_qty})


class CartUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, product_id):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = CartService(request.user)
        cart.update(product_id, serializer.validated_data['quantity'])

        data = cart.get_cart_detail()
        return Response(CartDetailSerializer(data).data)


class CartRemoveView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, product_id):
        cart = CartService(request.user)
        cart.remove(product_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartClearView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        cart = CartService(request.user)
        cart.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
