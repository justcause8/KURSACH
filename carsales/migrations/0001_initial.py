# Generated by Django 5.1.1 on 2024-09-15 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.TextField()),
                ('car_model', models.TextField()),
                ('year', models.TextField()),
                ('price', models.TextField()),
            ],
        ),
    ]
