# Generated by Django 5.1.1 on 2024-10-19 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_alter_articleentry_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleentry',
            name='img',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
