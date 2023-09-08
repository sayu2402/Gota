# Generated by Django 4.2.1 on 2023-08-03 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderss', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('New', 'New'), ('Accepted', 'Accepted'), ('Completed', 'Completed')], default='Now', max_length=100),
        ),
    ]
