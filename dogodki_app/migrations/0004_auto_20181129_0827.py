# Generated by Django 2.1.3 on 2018-11-29 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dogodki_app', '0003_skupina'),
    ]

    operations = [
        migrations.CreateModel(
            name='Povabilo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dogodek', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='povabljeni', to='dogodki_app.Dogodek')),
            ],
            options={
                'verbose_name': 'Povabilo',
                'verbose_name_plural': 'Povabila',
            },
        ),
        migrations.AlterField(
            model_name='skupina',
            name='dogodek',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skupine', to='dogodki_app.Dogodek'),
        ),
        migrations.AddField(
            model_name='povabilo',
            name='skupina',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prijavljeni', to='dogodki_app.Skupina'),
        ),
        migrations.AddField(
            model_name='povabilo',
            name='uporabnik',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]