# Generated by Django 5.1.2 on 2024-10-23 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_alter_buyerprofile_user_alter_sellerprofile_user'),
        ('wishlist', '0008_remove_wishlistitem_user_wishlistitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlistitem',
            name='user',
        ),
        migrations.AddField(
            model_name='wishlistitem',
            name='user',
            field=models.ManyToManyField(to='user_profile.buyerprofile'),
        ),
    ]
