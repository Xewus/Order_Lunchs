from datetime import date
from django.contrib.auth import get_user_model
from django.db.models import (SET_NULL, BooleanField, CharField,
                              DecimalField, ForeignKey, DateField,
                              TimeField, Model, ManyToManyField,
                              UniqueConstraint)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .validators import validate_only_one_instance

todey = date.today()
User = get_user_model()
WEEKDAYS = {
            '1': 'Понедельник',
            '2': 'Вторник',
            '3': 'Среда',
            '4': 'Четверг',
            '5': 'Пятница',
            '6': 'Суббота',
            '7': 'Воскресенье',
        }


class DeliveryDate(Model):
    """
    Хранит возможнве даты поставок.M2M
    """
    delivery_date = DateField(
        verbose_name='Дата поставки',
        unique=True
    )

    def __str__(self):
        return str(self.delivery_date)


class TypeFood(Model):
    """
    Укащывает вид блюда. M2M.
    """
    name = CharField(
        verbose_name='Тип блюда',
        max_length=20,
        unique=True,
    )

    class Meta:        
        verbose_name = 'Тип блюда'
        verbose_name_plural = 'Типы блюд'

    def __str__(self):
        return f'{self.name}'


class Dish(Model):
    name = CharField(
        verbose_name='Название блюда',
        max_length=100,
        unique=True
    )
    description = CharField(
        verbose_name='Описание блюда',
        max_length=500
    )
    price = DecimalField(
        verbose_name='Стоимость блюда',
        max_digits=7,
        decimal_places=2,
    )
    weight = DecimalField(
        verbose_name='Вес блюда',
        max_digits=8,
        decimal_places=3,
        default=0,
    )
    calories = DecimalField(
        verbose_name='Калории',
        max_digits=9,
        decimal_places=3,
        default=0,
    )
    vegan = BooleanField(
        verbose_name='Вегитарианская',
        default=False,
    )
    type_food = ForeignKey(
        verbose_name='Тип блюда',
        to=TypeFood,
        related_name='dishes',
        null=True,
        blank=True,
        on_delete=SET_NULL,
    )
    delivery_days = ManyToManyField(
        verbose_name='Дни для заказа',
        to=DeliveryDate,
        related_name='dishes',
        blank=True,
    )

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}. Стоимость: {self.price}.'

    @property
    def get_delivery_days(self):
        return  self.delivery_days.all()


class Order(Model):
    dish = ForeignKey(
        verbose_name='Блюда',
        to=Dish,
        related_name='orders',
        null=True,
        on_delete=SET_NULL,
   )
    customer = ForeignKey(
        verbose_name='Заказчик',
        to=User,
        related_name='orders',
        null=True,
        on_delete=SET_NULL,
    )
    delivery_date = DateField(
        verbose_name='Дата поступления заказа'
    )
    order_date = DateField(
        verbose_name='Дата оформления заказа',
        auto_now=True,
    )
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = (
            'delivery_date',
            'customer__last_name',
            'customer__first_name',
            'customer__patronymic',
        )
        constraints = (
            UniqueConstraint(
                fields=('dish', 'customer', 'delivery_date',),
                name='Разрешён один заказ в день.',

            ),
        )


class OrderTime(Model):
    """
    Ограничивает время заказов.
    """
    start_time = TimeField(
        verbose_name='Время начала приёма заказов',
        blank=True,
        null=True,
    )
    end_time = TimeField(
        verbose_name='Время окончания приёма заказов',
    )

    class Meta:        
        verbose_name = 'Ограничение времени заказов'
        verbose_name_plural = 'Ограничение времени заказов'

    def __str__(self):
        return f'Начало приёма: {self.start_time}, конец приёма: {self.end_time}.'

    def clean(self):
        validate_only_one_instance(self)

    @property
    def get_end_time_hour(self):
        return self.end_time.hour
