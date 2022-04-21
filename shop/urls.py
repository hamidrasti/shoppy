from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import BrandViewSet, CategoryViewSet, ProductViewSet, CartViewSet, CartItemViewSet, OrderViewSet

app_name = 'shop'

router = DefaultRouter()
router.register('brands', BrandViewSet, basename='brands')
router.register('categories', CategoryViewSet, basename='categories')
router.register('products', ProductViewSet, basename='products')
router.register('carts', CartViewSet, basename='carts')
router.register('orders', OrderViewSet, basename='orders')

carts_router = NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', CartItemViewSet, basename='cartitems')

urlpatterns = router.urls + carts_router.urls
