# Generated by Django 3.2 on 2021-06-17 02:12

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom1', '0003_alter_seller_seller_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
