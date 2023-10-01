from django.contrib import admin
from app.models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist, Product_Category
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import Group


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'description',
                    'selling_price', 'main_catetory', 'category', 'product_image']


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality',
                    'city', 'state', 'zipcode', 'mobile']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'razorpay_order_id',
                    'razorpay_payment_status', 'razorpay_payment_id', 'paid']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product',
                    'quantity', 'ordered_date', 'status', 'payment']


@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']

    def product(self, obj):
        link = reverse('admin:app_product_change', args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)


@admin.register(Product_Category)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


# if you want to unregister the model
admin.site.unregister(Group)
