from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    friendly_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name 


class Product(models.Model):
    sku = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, db_index=True)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, related_name='products',
        on_delete=models.SET_NULL,
        null=True
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True
    )
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, 
        related_name='product_images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.product.name + " Image"
