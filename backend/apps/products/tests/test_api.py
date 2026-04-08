import pytest
from decimal import Decimal
from apps.products.tests.factories import CategoryFactory, ProductFactory


@pytest.mark.django_db
class TestCategoryList:
    url = '/api/v1/categories/'

    def test_list_categories(self, api_client):
        CategoryFactory.create_batch(3)
        response = api_client.get(self.url)
        assert response.status_code == 200

    def test_inactive_categories_hidden(self, api_client):
        CategoryFactory(is_active=True, name='Visible')
        CategoryFactory(is_active=False, name='Hidden')
        response = api_client.get(self.url)
        names = [c['name'] for c in (response.data.get('results') or response.data)]
        assert 'Visible' in names
        assert 'Hidden' not in names


@pytest.mark.django_db
class TestProductList:
    url = '/api/v1/products/'

    def test_list_products(self, api_client):
        ProductFactory.create_batch(3)
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert response.data['count'] == 3

    def test_inactive_products_hidden(self, api_client):
        ProductFactory(is_active=True)
        ProductFactory(is_active=False)
        response = api_client.get(self.url)
        assert response.data['count'] == 1

    def test_filter_by_category(self, api_client):
        cat = CategoryFactory(slug='electronics')
        ProductFactory(category=cat)
        ProductFactory()  # different category
        response = api_client.get(self.url, {'category': 'electronics'})
        assert response.data['count'] == 1

    def test_filter_by_price_range(self, api_client):
        ProductFactory(price=Decimal('10.00'))
        ProductFactory(price=Decimal('50.00'))
        ProductFactory(price=Decimal('100.00'))
        response = api_client.get(self.url, {'min_price': 20, 'max_price': 60})
        assert response.data['count'] == 1

    def test_search_by_name(self, api_client):
        ProductFactory(name='Wireless Headphones')
        ProductFactory(name='USB Cable')
        response = api_client.get(self.url, {'search': 'wireless'})
        assert response.data['count'] == 1


@pytest.mark.django_db
class TestProductDetail:
    def test_retrieve_by_slug(self, api_client):
        product = ProductFactory(slug='test-product')
        response = api_client.get(f'/api/v1/products/{product.slug}/')
        assert response.status_code == 200
        assert response.data['name'] == product.name

    def test_404_for_nonexistent(self, api_client):
        response = api_client.get('/api/v1/products/nonexistent/')
        assert response.status_code == 404


@pytest.mark.django_db
class TestProductCRUDPermissions:
    url = '/api/v1/products/'

    def test_anon_cannot_create(self, api_client):
        cat = CategoryFactory()
        data = {
            'name': 'New Product', 'slug': 'new-product',
            'price': '29.99', 'stock': 10, 'category': cat.pk,
        }
        response = api_client.post(self.url, data)
        assert response.status_code in (401, 403)

    def test_normal_user_cannot_create(self, auth_client):
        cat = CategoryFactory()
        data = {
            'name': 'New Product', 'slug': 'new-product',
            'price': '29.99', 'stock': 10, 'category': cat.pk,
        }
        response = auth_client.post(self.url, data)
        assert response.status_code == 403

    def test_admin_can_create(self, admin_client):
        cat = CategoryFactory()
        data = {
            'name': 'Admin Product', 'slug': 'admin-product',
            'description': 'Created by admin', 'price': '29.99',
            'stock': 10, 'category': cat.pk,
        }
        response = admin_client.post(self.url, data)
        assert response.status_code == 201

    def test_soft_delete(self, admin_client):
        product = ProductFactory()
        response = admin_client.delete(f'/api/v1/products/{product.slug}/')
        assert response.status_code == 204
        product.refresh_from_db()
        assert product.is_active is False
