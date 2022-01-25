from django.db.models import BooleanField, CharField, DateField, Model, ForeignKey, CASCADE, SET_NULL


class Department(Model):
    name = CharField(
        verbose_name='Название отдела',
        max_length=200,
        unique=True,
    )

class Employer(Model):
    name = CharField(
        verbose_name='Имя сотрудника',
        max_length=50,
    )
    middlename = CharField(
        verbose_name='Отчество сотрудника',
        max_length=100,
    )
    surname = CharField(
        verbose_name='Фамилия сотрудника',
        max_length=100,
    )
    department = ForeignKey(
        verbose_name='Название отдела'
        to=Department,
        related_name='employees',
        on_delete=SET_NULL
    )


class Lunch(Model):
    content = CharField(
        verbose_name='Состав заказа',
        max_length=300,
    )
    add_date = DateField(
        verbose_name='Дата заказа',
        auto_now_add=True
    )
    customer = ForeignKey(
        verbose_name='Заказчик',
        to=Employer,
        related_name='lunches',
        on_delete=CASCADE,
    )
