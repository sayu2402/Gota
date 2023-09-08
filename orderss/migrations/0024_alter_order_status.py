# Generated by Django 4.2.1 on 2023-08-21 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderss', '0023_alter_order_order_product_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('New', 'New'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered')], default='New', max_length=100),
        ),
    ]