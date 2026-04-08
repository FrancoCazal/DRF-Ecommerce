import pytest
from apps.products.tests.factories import CategoryFactory, ProductFactory


@pytest.mark.django_db
class TestCategoryModel:
    def test_str(self):
        category = CategoryFactory(name='Electronics')
        assert str(category) == 'Electronics'

    def test_ordering(self):
        CategoryFactory(name='Zebra')
        CategoryFactory(name='Alpha')
        from apps.products.models import Category
        names = list(Category.objects.values_list('name', flat=True))
        assert names == ['Alpha', 'Zebra']


@pytest.mark.django_db
class TestProductModel:
    def test_str(self):
        product = ProductFactory(name='Test Widget')
        assert str(product) == 'Test Widget'

    def test_default_ordering_by_created_at_desc(self):
        p1 = ProductFactory(name='First')
        p2 = ProductFactory(name='Second')
        from apps.products.models import Product
        products = list(Product.objects.values_list('name', flat=True))
        assert products == ['Second', 'First']

    def test_category_protect_on_delete(self):
        product = ProductFactory()
        with pytest.raises(Exception):
            product.category.delete()
