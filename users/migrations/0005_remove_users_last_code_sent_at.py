# Generated by Django 4.0 on 2024-01-31 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_users_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='last_code_sent_at',
        ),
    ]