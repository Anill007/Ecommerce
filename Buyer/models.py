from django.db import models
from Ecom1.models import Product, Seller
import datetime

# Create your models here.


class Buyer(models.Model):
    class Meta:
        verbose_name_plural = "Buyers"

    buyer_id = models.AutoField(primary_key=True)
    buyer_name = models.CharField(max_length=50)
    buyer_password = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.buyer_id}'


class Cart(models.Model):
    class Meta:
        verbose_name_plural = "Carts"

    cart_id = models.AutoField(primary_key=True)
    buyer_id = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.cart_id}'


status_choices = (("CANCELLED", "Cancelled"), ("PENDING", "Pending"), ("APPROVED",
                  "Approved"), ("SUCCESS", "Success"))


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order_placed = models.DateTimeField(
        auto_now_add=True, auto_now=False)
    order_status = models.CharField(
        max_length=20, choices=status_choices, default="PENDING")

    def __str__(self):
        return f'{self.order_id}'

    class Meta:
        verbose_name_plural = "Orders"
