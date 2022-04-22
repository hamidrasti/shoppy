from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from .models import Product, Brand, Category, CartItem, Cart, OrderItem, Order

User = get_user_model()


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        read_only_fields = ('id', 'brand', 'category')
        fields = ('id', 'title', 'description', 'price', 'price_currency', 'size', 'color', 'brand', 'category',)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        read_only_fields = ('id',)
        fields = ('id', 'title', 'price',)


class CreateProductSerializer(ProductSerializer):
    brand_id = serializers.IntegerField(write_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        read_only_fields = ('id', 'brand', 'category')
        fields = (
            'id', 'title', 'description', 'price', 'price_currency', 'size', 'color', 'brand', 'category',
            'brand_id', 'category_id',
        )

    def save(self, **kwargs):
        # price = self.validated_data.pop('price')
        # price_currency = self.validated_data.pop('price_currency')
        brand_id = self.validated_data.pop('brand_id')
        category_id = self.validated_data.pop('category_id')

        try:
            brand = Brand.objects.get(pk=brand_id)
        except Brand.DoesNotExist:
            raise serializers.ValidationError('No brand with the given ID was found.')

        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError('No category with the given ID was found.')

        self.instance = Product.objects.create(
            brand=brand,
            category=category,
            # price=Money(price, price_currency),
            **self.validated_data
        )

        return self.instance


class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'price_currency', 'size', 'color',)


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    price_currency = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        read_only_fields = ('id',)
        fields = ('id', 'product', 'quantity', 'price_currency', 'total_price',)

    def get_price_currency(self, cart_item: CartItem):
        return str(cart_item.product.price.currency)

    def get_total_price(self, cart_item: CartItem):
        total = cart_item.quantity * cart_item.product.price
        return total.amount


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    price_currency = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        read_only_fields = ('id',)
        fields = ('id', 'items', 'price_currency', 'total_price',)

    def get_price_currency(self, cart: Cart):
        for item in cart.items.all():
            return str(item.product.price.currency)
        return 'IRR'

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.price.amount for item in cart.items.all()])


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        read_only_fields = ('id',)
        fields = ('id', 'product_id', 'quantity',)


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('quantity',)


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'unit_price', 'unit_price_currency', 'quantity', 'total_price',)

    def get_total_price(self, order_item: OrderItem):
        return order_item.quantity * order_item.product.price.amount


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    price_currency = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        read_only_fields = ('id',)
        fields = ('id', 'user', 'placed_at', 'status', 'items', 'price_currency', 'total_price',)

    def get_price_currency(self, order: Order):
        for item in order.items.all():
            return str(item.product.price.currency)
        return 'IRR'

    def get_total_price(self, order: Order):
        return sum([item.quantity * item.product.price.amount for item in order.items.all()])


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


# noinspection PyAbstractClass
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart with the given ID was found.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']

            user = User.objects.get(pk=self.context['user_id'])
            order = Order.objects.create(user=user)

            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.price,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()

            return order
