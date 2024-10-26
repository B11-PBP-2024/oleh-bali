# Generated by Django 5.1.2 on 2024-10-22 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_remove_productentry_product_dataset_and_more'),
        ('user_profile', '0006_alter_buyerprofile_user_alter_sellerprofile_user'),
        ('wishlist', '0006_rename_buyers_wishlistitem_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistitem',
            name='products',
            field=models.ManyToManyField(to='seller.productentry'),
        ),
        migrations.AlterField(
            model_name='wishlistitem',
            name='user',
            field=models.ManyToManyField(to='user_profile.buyerprofile'),
        ),
    ]