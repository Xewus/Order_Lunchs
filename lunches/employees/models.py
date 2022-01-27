
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models import (SET_NULL, BooleanField, CharField,
                              CheckConstraint, DateTimeField,
                              DecimalField, EmailField, ForeignKey,
                              Model, Q)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class Department(Model):
    name = CharField(
        verbose_name='Название отдела',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'


class Employer(AbstractBaseUser, PermissionsMixin):
    first_name = CharField(
        verbose_name=_('Имя сотрудника'),
        max_length=50,
    )
    patronymic = CharField(
        verbose_name='Отчество сотрудника',
        max_length=100,
    )
    last_name = CharField(
        verbose_name='Фамилия сотрудника',
        max_length=50,
    )
    email = EmailField(
        verbose_name='Адрес электронной почты',
        max_length=50,
        unique=True,
    )
    is_staff = BooleanField(
        verbose_name=_('Администратор'),
        default=False,
        help_text=_('Разрешает пользоваться админкой'),
    )
    is_active = BooleanField(
        verbose_name=_('Действующий сотрудник'),
        default=True,
        help_text=_('Разрешает совершать заказы'),
    )
    department = ForeignKey(
        verbose_name='Название отдела',
        to=Department,
        related_name='employees',
        null=True,
        blank=True,
        on_delete=SET_NULL,
    )
    balance = DecimalField(
        verbose_name='Баланс',
        default=0,
        max_digits=7,
        decimal_places=2,
    )
    overdraft = BooleanField(
        verbose_name='Разрешить отрицательный баланс',
        default=False,
    )
    date_joined = DateTimeField(
        verbose_name= _('Дата регистрации'),
         default=timezone.now,
    )
    last_login = DateTimeField(
        verbose_name=_('Последнее посещение'),
        default=timezone.now,
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('password',)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ('last_name', 'first_name', 'patronymic',)
        constraints = (
            CheckConstraint(
                check=(Q(balance__gte=0) | Q(overdraft=True)),
                name='Отрицательный баланс не разрешён',

            ),
        )

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email}). Отдел: "{self.department}"'

    @property
    def full_name(self):
        return f'{self.first_name} {self.patronymic} {self.last_name}'
