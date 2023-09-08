# Generated by Django 4.2.1 on 2023-08-21 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderss', '0026_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('New', 'New'), ('Cancelled', 'Cancelled'), ('Shipped', 'Shipped')], default='New', max_length=100),
        ),
    ]
