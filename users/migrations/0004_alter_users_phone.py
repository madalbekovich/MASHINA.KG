# Generated by Django 4.0 on 2024-01-31 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_users_last_code_sent_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.CharField(max_length=16, unique=True, verbose_name='Номер телефона'),
        ),
    ]