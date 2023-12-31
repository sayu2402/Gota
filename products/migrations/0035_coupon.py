# Generated by Django 4.2.1 on 2023-08-21 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0034_alter_variation_variation_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=10)),
                ('is_expired', models.BooleanField(default=False)),
                ('discount_price', models.IntegerField(default=100)),
                ('minimum_amount', models.IntegerField(default=1500)),
            ],
        ),
    ]
