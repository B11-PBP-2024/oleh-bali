# Generated by Django 5.1.2 on 2024-10-18 08:44

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productentry',
            name='product_category',
            field=models.CharField(choices=[('Textile', 'Textile'), ('Art', 'Art'), ('Handicraft', 'Handicraft'), ('Traditional Wear', 'Traditional Wear'), ('Food', 'Food'), ('Jewelry', 'Jewelry'), ('Souvenir', 'Souvenir'), ('Accessory', 'Accessory'), ('Traditional Weapon', 'Traditional Weapon'), ('Musical Instrument', 'Musical Instrument'), ('Beverage', 'Beverage'), ('Art', 'Art')], default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productentry',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]