# Generated by Django 3.0.8 on 2020-10-24 04:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0004_auto_20201011_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
