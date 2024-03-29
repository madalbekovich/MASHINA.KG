# Generated by Django 4.0 on 2024-01-24 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactscars',
            name='user_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ContactsCar', to='users.users', verbose_name='Номер телефона'),
        ),
        migrations.AddField(
            model_name='carmodel',
            name='mark',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.carbrand'),
        ),
        migrations.AddField(
            model_name='cararea',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.carregion'),
        ),
        migrations.AddField(
            model_name='addinfocar',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.passengercars'),
        ),
    ]
