# Generated by Django 3.2 on 2021-05-08 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Ecom1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('buyer_id', models.AutoField(primary_key=True, serialize=False)),
                ('buyer_name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Buyers',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1)),
                ('order_placed', models.DateTimeField(auto_now_add=True)),
                ('order_status', models.CharField(choices=[('CANCELLED', 'Cancelled'), ('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('SUCCESS', 'Success')], default='PENDING', max_length=20)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.buyer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ecom1.product')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ecom1.seller')),
            ],
            options={
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_quantity', models.IntegerField(default=1)),
                ('buyer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.buyer')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ecom1.product')),
            ],
            options={
                'verbose_name_plural': 'Carts',
            },
        ),
    ]
