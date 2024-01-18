# Generated by Django 4.0 on 2024-01-17 12:28

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Brand')),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50, verbose_name='Модель')),
                ('mark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.carbrand')),
            ],
        ),
        migrations.CreateModel(
            name='PassengerCars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('some_field', models.CharField(max_length=50)),
                ('location', models.CharField(choices=[('Бишкек', 'Бишкек'), ('Нарын', 'Нарын'), ('Талас', 'Талас'), ('Ыссык-көл', 'Ыссык-көл'), ('Баткен', 'Баткен'), ('Жалал-абад', 'Жалал-абад'), ('Ош', 'Ош')], max_length=50, verbose_name='Где находится')),
                ('car_year', models.DateTimeField()),
                ('fuel', models.CharField(choices=[('БЕНЗИН', 'Бензин'), ('Дизель', 'Дизель')], max_length=10)),
                ('mileage', models.BigIntegerField()),
                ('mark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.carbrand')),
                ('model', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='mark', chained_model_field='mark', on_delete=django.db.models.deletion.CASCADE, to='marketplace.carmodel')),
            ],
            options={
                'verbose_name': 'Пассажирский автомобиль',
                'verbose_name_plural': 'Пассажирские автомобили',
            },
        ),
    ]
