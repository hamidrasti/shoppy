from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField

User = get_user_model()


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Colors(models.TextChoices):
        NONE = ('none', 'None')
        RED = ('red', 'Red')
        GREEN = ('green', 'Green')
        BLUE = ('blue', 'Blue')

    class Sizes(models.TextChoices):
        NONE = ('none', 'None')
        SMALL = ('small', 'Small')
        MEDIUM = ('medium', 'Medium')
        LARGE = ('large', 'Large')

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='IRR')
    image = models.ImageField(upload_to='products', null=True, blank=True)
    color = models.CharField(max_length=255, choices=Colors.choices, default=Colors.NONE)
    size = models.CharField(max_length=255, choices=Sizes.choices, default=Sizes.NONE)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [('cart', 'product')]


class Order(models.Model):
    class Status(models.TextChoices):
        PREPARING = ('preparing', 'Preparing')
        PREPARED = ('prepared', 'Prepared')
        SENT = ('sent', 'Sent')
        CANCELED = ('canceled', 'Canceled')
        REFERRED = ('referred', 'Referred')
        DELIVERED = ('delivered', 'Delivered')

    placed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.PREPARING)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
