# Generated by Django 5.1.1 on 2024-10-26 05:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_articleentry_img'),
        ('user_profile', '0009_alter_buyerprofile_nationality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleentry',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.buyerprofile'),
        ),
    ]