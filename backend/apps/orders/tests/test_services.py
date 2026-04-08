import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock
from rest_framework.exceptions import ValidationError
from apps.orders.services import CheckoutService
from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from apps.products.tests.factories import ProductFactory


class FakeCartService:
    """Mock CartService that returns predetermined items."""

    def __init__(self, items=None):
        self._items = items or []
        self.cleared = False

    def get_items(self):
        return self._items

    def clear(self):
        self.cleared = True


@pytest.mark.django_db
class TestCheckoutService:
    def _make_service(self, user, cart_items):
        service = CheckoutService(user)
        service.cart_service = FakeCartService(cart_items)
        return service

    def test_create_order_success(self, user):
        p1 = ProductFactory(price=Decimal('10.00'), stock=50)
        p2 = ProductFactory(price=Decimal('25.00'), stock=30)
        cart_items = [
            {'product_id': p1.id, 'quantity': 2},
            {'product_id': p2.id, 'quantity': 1},
        ]
        service = self._make_service(user, cart_items)
        order = service.create_order(shipping_address='123 Main St')

        assert order.user == user
        assert order.total_amount == Decimal('45.00')
        assert order.shipping_address == '123 Main St'
        assert order.status == Order.Status.PENDING
        assert order.items.count() == 2

        p1.refresh_from_db()
        p2.refresh_from_db()
        assert p1.stock == 48
        assert p2.stock == 29

        assert service.cart_service.cleared

    def test_empty_cart_raises(self, user):
        service = self._make_service(user, [])
        with pytest.raises(ValidationError, match='empty'):
            service.create_order()

    def test_insufficient_stock_raises(self, user):
        p = ProductFactory(price=Decimal('10.00'), stock=2)
        cart_items = [{'product_id': p.id, 'quantity': 5}]
        service = self._make_service(user, cart_items)
        with pytest.raises(ValidationError, match='Insufficient stock'):
            service.create_order()

        p.refresh_from_db()
        assert p.stock == 2  # stock unchanged

    def test_inactive_product_raises(self, user):
        p = ProductFactory(is_active=False, stock=50)
        cart_items = [{'product_id': p.id, 'quantity': 1}]
        service = self._make_service(user, cart_items)
        with pytest.raises(ValidationError, match='not available'):
            service.create_order()

    def test_nonexistent_product_raises(self, user):
        cart_items = [{'product_id': 99999, 'quantity': 1}]
        service = self._make_service(user, cart_items)
        with pytest.raises(ValidationError, match='not available'):
            service.create_order()
