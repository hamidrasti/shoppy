from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from .models import Category, Brand, Product


class BrandNode(DjangoObjectType):
    class Meta:
        model = Brand
        interfaces = (Node,)
        fields = '__all__'
        filter_fields = ['name']


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (Node,)
        fields = '__all__'
        filter_fields = ['name']


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        # Allow for some more advanced filtering here
        interfaces = (Node,)
        fields = '__all__'
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains'],
            'category': ['exact'],
            'category_id': ['exact'],
            'category__name': ['exact'],
            'color': ['exact'],
            'brand_id': ['exact'],
            'price': ['gte', 'lte'],
        }


class Query(object):
    brand = Node.Field(BrandNode)
    brands = DjangoFilterConnectionField(BrandNode)

    category = Node.Field(CategoryNode)
    categories = DjangoFilterConnectionField(CategoryNode)

    product = Node.Field(ProductNode)
    products = DjangoFilterConnectionField(ProductNode)
