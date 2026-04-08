from rest_framework import serializers


class CartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    product_slug = serializers.SlugField()
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    product_image = serializers.URLField(allow_null=True)
    quantity = serializers.IntegerField()
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2)


class CartDetailSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    count = serializers.IntegerField()


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
