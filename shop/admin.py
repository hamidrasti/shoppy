from django.contrib import admin

from .models import Product, Brand, Category


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'color', 'size', 'brand', 'category')
    list_select_related = ('brand', 'category')
    autocomplete_fields = ('brand', 'category')
