# Generated by Django 5.1.2 on 2024-10-26 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0008_alter_productseller_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productseller',
            name='price',
            field=models.IntegerField(),
        ),
    ]