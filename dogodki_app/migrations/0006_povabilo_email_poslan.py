# Generated by Django 2.1.3 on 2019-01-14 22:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dogodki_app', '0005_user_oddelek'),
    ]

    operations = [
        migrations.AddField(
            model_name='povabilo',
            name='email_poslan',
            field=models.BooleanField(default=False),
        ),
    ]
