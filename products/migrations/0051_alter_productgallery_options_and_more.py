# Generated by Django 4.2.1 on 2023-09-06 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0050_rename_images_productgallery_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productgallery',
            options={'verbose_name': 'productgallery', 'verbose_name_plural': 'product gallery'},
        ),
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('size', 'size'), ('color', 'color')], max_length=100),
        ),
    ]
