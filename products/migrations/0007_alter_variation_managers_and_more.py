# Generated by Django 4.2.1 on 2023-08-01 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_variation_variation_category'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='variation',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('size', 'size'), ('color', 'color')], max_length=100),
        ),
    ]
