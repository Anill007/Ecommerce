# Generated by Django 3.2 on 2021-05-03 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom1', '0009_delete_order'),
        ('Buyer', '0002_cart_product_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.buyer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ecom1.product')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ecom1.seller')),
            ],
            options={
                'verbose_name_plural': 'Orders',
            },
        ),
    ]