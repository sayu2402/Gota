# Generated by Django 4.2.1 on 2023-08-23 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderss', '0030_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('New', 'New')], default='New', max_length=100),
        ),
    ]
