# Generated by Django 5.1.2 on 2024-10-19 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0002_remove_wishlistitem_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlistitem',
            name='price',
        ),
        migrations.AddField(
            model_name='wishlistitem',
            name='max_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='wishlistitem',
            name='min_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]