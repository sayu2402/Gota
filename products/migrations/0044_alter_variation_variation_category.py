# Generated by Django 4.2.1 on 2023-09-02 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0043_alter_variation_variation_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('color', 'color'), ('size', 'size')], max_length=100),
        ),
    ]
