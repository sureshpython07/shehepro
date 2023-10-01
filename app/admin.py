from django.contrib import admin
from app.models import Product, Product_Category


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'description',
                    'selling_price', 'main_catetory', 'category', 'product_image']


@admin.register(Product_Category)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
