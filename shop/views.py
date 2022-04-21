from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .filters import ProductFilterSet
from .models import Product, Brand, Category, CartItem, Cart, Order
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer, ProductSerializer, BrandSerializer, CartItemSerializer,
    UpdateCartItemSerializer, AddCartItemSerializer, CartSerializer, CreateOrderSerializer, OrderSerializer,
    UpdateOrderSerializer, CreateProductSerializer, UpdateProductSerializer
)

User = get_user_model()


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    serializer_class = BrandSerializer

    class Meta:
        model = Brand


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    serializer_class = CategorySerializer

    class Meta:
        model = Category


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilterSet
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['price']

    class Meta:
        model = Product

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateProductSerializer
        elif self.request.method == 'PATCH':
            return UpdateProductSerializer
        return ProductSerializer


class CartViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        user_id = User.objects.only('id').get(pk=user.id)
        return Order.objects.filter(user_id=user_id)

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id': self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
