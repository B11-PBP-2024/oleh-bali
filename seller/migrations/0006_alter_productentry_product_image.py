# Generated by Django 5.1.2 on 2024-10-24 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0005_merge_20241024_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productentry',
            name='product_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
