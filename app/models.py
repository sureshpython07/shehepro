from django.db import models

MAIN_CATEGORY = (
    ('Men', 'Men'),
    ('Women', 'Women'),
    ('Dairy', 'Dairy'),
)

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


class Product_Category(models.Model):
    name = models.CharField(choices=MAIN_CATEGORY, max_length=100)

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
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=100)
    product_size = models.CharField(
        choices=PRODUCT_SIZE_CHOICE, max_length=100)
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
