# Generated by Django 5.1.2 on 2024-10-22 18:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_seller'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewentry',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.buyer'),
        ),
    ]
