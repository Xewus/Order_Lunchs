"""Модуль представлений.

Для уменьшения количества строк следует понимать, что
каждое представление имеет не указанные в документации аргументы:
    title - Название страницы;
    template - html-шаблон страницы;
    context - словарь контекста передавемый в шаблон;
    user<опционально> - пользователь, отправивший запрос.
"""
from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import redirect, render

from .models import Dish, Order
from .services import end_time_accept_order, get_delivery_date, start_day_accept_order


User = get_user_model()


def index(request):
    """Показывает главную страницу сайта.
    """
    title = 'Главная страница'
    template = 'dishes/index.html'
    context = {
        'title': title,
        'text': 'Главная страница',
        'start_allow_days':start_day_accept_order(),
    }
    return render(request, template, context)


@login_required
def profile_orders(request, id, order_id=None):
    """Просмотр заказов пользователя.
    
    Если `order_id=None` возвращает список заказов.
    Если `order_id=<int>`, то передаёт данные конкретного заказа,
    а `one_order_page` указывает шаблону развернуть заказ.

    Args:
        request (WSGIRequest):
            Поступивший объект запроса.
        id (int):
            id пользователя, на которого поступил запрос.
        order_id (int):
            id заказа, который необходимо обработать, если нет,
            то обрабатываются все заказы запрошенного пользователя.
        query_res (QuerySet):
            Список результатов запроса к БД.
        one_order_page (bool):
            указание шаблону развернуть заказ для показа.
        

    Returns:
        obj (datetime): Календарная дата доставки.
    """
    title = 'Список Ваших заказов'
    template = 'dishes/order_list.html'
    user = request.user
    query_res = Order.objects.filter(customer=user)
    one_order_page = False

    if order_id:
        query_res = Dish.objects.filter(
            orders=order_id,
            orders__customer=user
        )
        one_order_page = True

    context = {
        'title': title,
        'user': user,
        'query_res': query_res,
        'one_order_page': one_order_page
    }
    return render(request, template, context)


@login_required
def profile(request, id):

    user = request.user
    title = f'Страница сотрудника {user.full_name}'
    template = 'dishes/profile.html'
    department = user.department
    dishes = Dish.objects.filter(orders__customer=user, orders__order_date=date.today())
    summa = sum(dish.price for dish in dishes)

    context = {
        'title': title,
        'user': user,
        'department': department,
        'dishes': dishes,
        'summa': summa,
        'end_time_accept_order()': end_time_accept_order(),
    }
    
    if request.method == 'GET':
        return render(request, template, context)
    
    if request.method == 'POST':
        on_dishes = set(dish for dish, order in request.POST.items() if order == 'on')
        on_dishes = Dish.objects.filter(
            name__in=on_dishes,
            orders__customer=user,
            orders__order_date=date.today()
        )
        summa = sum(dish.price for dish in on_dishes)
        user.balance = user.balance + summa
        user.save()
        Order.objects.filter(customer=user, dish__in=on_dishes).delete()

    return redirect('dishes:profile', user.id)


@login_required
def list_dishes(request, order_day):
    user = request.user
    title = 'Страница просмотра блюд'
    balance = (user.balance > 0 or user.overdraft)
    dishes = None
    week_days = '1,2,3,4,5, 8,9,10,11,12'
    allow_order = bool(str(order_day) in week_days)
    template = 'dishes/dishes.html'
    context = {
        'title': title,
        'balance': balance,
        'dishes': dishes,
        'allow_order': allow_order
    }

    if not balance:
        return redirect('dishes:index')

    allow_days = week_days[start_day_accept_order():]

    delivery_date = get_delivery_date(order_day)

    # or_filter = Q()
    # for day in allow_days:
    #     or_filter |=Q(order_days__contains=day)

    dishes = Dish.objects.filter(
        delivery_days__delivery_date=delivery_date,
    ).exclude(
        Q(orders__customer=user,
        delivery_days__delivery_date=delivery_date)
    )

    # if allow_order:
    #     and_filter = Q(order_days__contains=order_day)
    #     dishes = dishes.filter(and_filter)
    
    context['dishes'] = dishes

    if request.method == 'GET':
        return render(request, template, context)


    if request.method == 'POST':
        on_dishes = set(dish for dish, order in request.POST.items() if order == 'on')
        on_dishes = Dish.objects.filter(
            name__in=on_dishes
        ).exclude(
            orders__customer=user, orders__delivery_date=date.today()
        )
        summa = sum(dish.price for dish in on_dishes)
        if not user.overdraft and summa > user.balance:
            context['balance'] = False
            return render(request, template, context)
        orders = [
            Order(
                dish=dish,
                customer=user,
                delivery_date = get_delivery_date(order_day),
                order_date=date.today()
            ) for dish in on_dishes
        ]
        Order.objects.bulk_create(orders)
        user.balance = user.balance - summa
        user.save()
        return redirect('dishes:profile', user.id)

    return redirect('dishes:index')
