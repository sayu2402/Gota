# Generated by Django 4.2.1 on 2023-08-05 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderss', '0009_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('New', 'New'), ('Cancelled', 'Cancelled'), ('Shipped', 'Shipped')], max_length=100),
        ),
    ]
