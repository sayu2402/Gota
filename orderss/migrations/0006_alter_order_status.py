# Generated by Django 4.2.1 on 2023-08-05 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderss', '0005_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Accepted', 'Accepted'), ('Completed', 'Completed'), ('New', 'New'), ('Shipped', 'Shipped')], default='New', max_length=100),
        ),
    ]
