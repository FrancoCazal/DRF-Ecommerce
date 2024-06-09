from rest_framework.routers import DefaultRouter
from .views.product_viewsets import ProductViewset
from apps.products.api.views.general_views import *

router = DefaultRouter()

# Obs: es necesario especificar el basename para def_queryset
router.register(r'products',ProductViewset, basename = 'products')
router.register(r'measure_unit',MeasureUnitViewset, basename = 'measure_unit')
router.register(r'indicators',IndicatorViewset, basename = 'indicators')
router.register(r'category_products',CategoryProductViewset, basename = 'category_products')

# Necesario asignar para cuando se busque en el archivo
urlpatterns = router.urls