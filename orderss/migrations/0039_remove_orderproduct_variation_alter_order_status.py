# Generated by Django 4.2.1 on 2023-09-02 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderss', '0038_order_quantity_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variation',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('New', 'New'), ('Shipped', 'Shipped')], default='New', max_length=100),
        ),
    ]