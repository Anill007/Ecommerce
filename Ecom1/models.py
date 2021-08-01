from django.db import models
import os
from cloudinary.models import CloudinaryField

# Create your models here.


class Seller(models.Model):
    class Meta:
        verbose_name_plural = "Sellers"

    seller_id = models.AutoField(primary_key=True)
    seller_name = models.CharField(max_length=50)
    seller_password = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.seller_id}'


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_image = models.ImageField()
    product_details = models.CharField(max_length=100)
    product_price = models.FloatField()
    product_model = models.CharField(max_length=100)
    product_category = models.CharField(max_length=50)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product_id}'

    def delete(self, *args, **kwargs):
        path_str = self.product_image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Products"
