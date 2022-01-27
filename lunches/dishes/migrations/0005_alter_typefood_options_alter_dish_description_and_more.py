# Generated by Django 4.0.1 on 2022-01-27 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0004_alter_ordertime_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='typefood',
            options={'verbose_name': 'Тип блюда', 'verbose_name_plural': 'Типы блюд'},
        ),
        migrations.AlterField(
            model_name='dish',
            name='description',
            field=models.CharField(max_length=500, verbose_name='Описание блюда'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='order_days',
            field=models.CharField(max_length=7, verbose_name='Дни для заказа'),
        ),
    ]