from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = (
    ('TRACKPANT', 'TRACKPANT'),
    ('PALAZZO', 'PALAZZO'),
    ('LJEANS', 'LEDIES JEANS'),
    ('GJEANS', 'GENTS JEANS'),
    ('SHIRT', 'SHIRT'),
    ('PANT', 'PANT'),
    ('SHORTS', 'SHORTS'),
    ('SKIRT', 'SKIRT'),
    ('INNER', 'INNER'),
    ('SAREE', 'SAREE'),
    ('JACKET', 'JACKET'),
    ('LEGGING', 'LEGGING'),
    ('CURD', 'CURD'),
    ('MILK', 'MILK'),
    ('LASSI', 'LASSI'),
    ('MILKSHAKE', 'MILKSHAKE'),
    ('GHEE', 'GHEE'),
    ('PANEER', 'PANEER'),
    ('CHEESE', 'CHEESE'),
    ('ICE', 'ICE-CREAME'),
)
PRODUCT_SIZE_CHOICE = (
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
)

STATE_CHOICE = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
)

ORDER_STATUS_CHOICE = (('PENDING', 'PENDING'),
                       ('ORDER_PROCESSING', 'ORDER PROCESSING'),
                       ('SHIPPING', 'SHIPPING'),
                       ('PENDING', 'PENDING'),
                       ('OUT_FOR_DELIVERY', 'OUT FOR DELIVERY'),
                       ('DELIVERED', 'DELIVERED'),
                       ('CANCEL', 'CANCEL')
                       )

MAIN_CATEGORY = (
    ('Men', 'Men'),
    ('Women', 'Women'),
    ('Dairy', 'Dairy'),
)


class Product_Category(models.Model):
    name = models.CharField(choices=MAIN_CATEGORY)

    def __str__(self):
        return self.name

    @staticmethod
    def get_category_all():
        return Product_Category.objects.all()


class Product(models.Model):
    title = models.CharField(max_length=255)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    main_catetory = models.ForeignKey(
        Product_Category, on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORY_CHOICES)
    product_size = models.CharField(choices=PRODUCT_SIZE_CHOICE)
    product_image = models.ImageField(upload_to='product_image')

    def __str__(self):
        return self.title

    @staticmethod
    def get_products_all():
        return Product.objects.all()

    @staticmethod
    def get_all_product_by_category_id(category_id):
        if category_id:
            return Product.objects.values(
                'id', 'title', 'discounted_price', 'selling_price',
                'product_image').filter(main_catetory=category_id)
        else:
            return Product.get_products_all()


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    mobile = models.IntegerField()
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICE, max_length=100)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cast(self):
        return self.quantity * self.product.discounted_price


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(
        max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(
        max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=ORDER_STATUS_CHOICE, max_length=100, default='PENDING')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    @property
    def total_cast(self):
        return self.quantity * self.product.discounted_price


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    encrypt_id = models.CharField(max_length=255)
