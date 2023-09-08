# Generated by Django 4.2.1 on 2023-09-06 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderss', '0050_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered')], default='New', max_length=100),
        ),
    ]
