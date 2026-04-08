import redis
from decimal import Decimal
from django.conf import settings
from apps.products.models import Product


class CartService:
    """
    Redis-backed cart. Each user's cart is a Redis hash at key
    'cart:user:{user_id}', where field = product_id, value = quantity.
    """

    def __init__(self, user):
        self.user = user
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.key = f'cart:user:{user.id}'

    def _refresh_ttl(self):
        self.redis.expire(self.key, settings.CART_TTL)

    def get_items(self):
        raw = self.redis.hgetall(self.key)
        return [
            {'product_id': int(pid), 'quantity': int(qty)}
            for pid, qty in raw.items()
        ]

    def add(self, product_id, quantity=1):
        new_qty = self.redis.hincrby(self.key, str(product_id), quantity)
        self._refresh_ttl()
        return new_qty

    def update(self, product_id, quantity):
        if quantity <= 0:
            return self.remove(product_id)
        self.redis.hset(self.key, str(product_id), quantity)
        self._refresh_ttl()
        return quantity

    def remove(self, product_id):
        self.redis.hdel(self.key, str(product_id))
        self._refresh_ttl()

    def clear(self):
        self.redis.delete(self.key)

    def get_cart_detail(self):
        items = self.get_items()
        if not items:
            return {'items': [], 'total': Decimal('0.00'), 'count': 0}

        product_ids = [item['product_id'] for item in items]
        products = Product.objects.filter(
            id__in=product_ids, is_active=True,
        ).in_bulk()

        cart_items = []
        total = Decimal('0.00')
        for item in items:
            product = products.get(item['product_id'])
            if product is None:
                self.remove(item['product_id'])
                continue
            line_total = product.price * item['quantity']
            total += line_total
            cart_items.append({
                'product_id': product.id,
                'product_name': product.name,
                'product_slug': product.slug,
                'product_price': product.price,
                'product_image': product.image.url if product.image else None,
                'quantity': item['quantity'],
                'line_total': line_total,
            })

        return {
            'items': cart_items,
            'total': total,
            'count': sum(i['quantity'] for i in cart_items),
        }
