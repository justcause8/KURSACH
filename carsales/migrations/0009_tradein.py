# Generated by Django 5.1 on 2024-12-13 18:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carsales', '0008_car_user_customer_user_dealer_user_dealercenter_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_model', models.CharField(max_length=100, verbose_name='Модель автомобиля')),
                ('year', models.PositiveIntegerField(verbose_name='Год выпуска')),
                ('mileage', models.PositiveIntegerField(verbose_name='Пробег')),
                ('price', models.TextField(null=True, verbose_name='Цена автомобиля')),
                ('additional_info', models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата подачи заявки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Трейд-ин заявка',
                'verbose_name_plural': 'Трейд-ин заявки',
            },
        ),
    ]
