# Generated by Django 4.2.1 on 2023-08-03 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderss', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('New', 'New')], default='Now', max_length=100),
        ),
    ]