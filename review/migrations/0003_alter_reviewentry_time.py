# Generated by Django 5.1.2 on 2024-10-22 19:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_alter_reviewentry_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewentry',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]