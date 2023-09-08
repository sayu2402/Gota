# Generated by Django 4.2.1 on 2023-08-23 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderss', '0033_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('New', 'New'), ('Shipped', 'Shipped')], default='New', max_length=100),
        ),
    ]
