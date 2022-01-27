from datetime import date
from datetime import datetime as dt

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import redirect, render

from .models import Dish, Order, OrderTime


end_time = 12
week_day = dt.now().weekday()
start_allow_days = (
    week_day + 1 + int(dt.now().hour > end_time)
)
User = get_user_model()


def index(request):
    title = 'Главная страница'
    context = {
        'title': title,
        'text': 'Главная страница',
        'start_allow_days':start_allow_days,
    }
    template = 'dishes/index.html'
    return render(request, template, context)

@login_required
def profile(request, id):
    user = request.user
    department = user.department
    dishes = Dish.objects.filter(orders__customer=user, orders__order_date=dt.now())
    summa = sum(dish.price for dish in dishes)


    title = f'Страница заказов сотрудника {user.full_name}'
    template = 'dishes/profile.html'
    context = {
        'title': title,
        'user': user,
        'department': department,
        'dishes': dishes,
        'summa': summa,
        'end_time': end_time,
    }
    
    if request.method == 'GET':
        return render(request, template, context)
    
    if request.method == 'POST':
        on_dishes = set(dish for dish, order in request.POST.items() if order == 'on')
        on_dishes = Dish.objects.filter(
            name__in=on_dishes,
            orders__customer=user,
            orders__order_date=dt.now()
        )
        summa = sum(dish.price for dish in on_dishes)
        user.balance = user.balance + summa
        user.save()
        Order.objects.filter(customer=user, dish__in=on_dishes).delete()

    return redirect('dishes:profile', user.id)


@login_required
def list_dishes(request, order_day=''):
    week_days = '12345'
    allow_order = bool(order_day in week_days)
    user = request.user
    balance = user.balance > 0
    dishes = None
    title = 'Страница просмотра блюд'
    template = 'dishes/dishes.html'
    context = {
        'title': title,
        'balance': balance,
        'dishes': dishes,
        'allow_order': allow_order
    }

    if not user.overdraft and not balance:
        return redirect('dishes:profile', user.id)

    allow_days = week_days[week_day:]
    or_filter = Q()
    for day in allow_days:
        or_filter |=Q(order_days__contains=day)

    dishes = Dish.objects.exclude(
        orders__customer=user
    ).filter(
        or_filter
    )

    if allow_order:
        and_filter = Q(order_days__contains=order_day)
        dishes = dishes.filter(and_filter)
    
    context['dishes'] = dishes

    if request.method == 'GET':
        return render(request, template, context)


    if request.method == 'POST':
        on_dishes = set(dish for dish, order in request.POST.items() if order == 'on')
        on_dishes = Dish.objects.filter(
            name__in=on_dishes
        ).exclude(
            orders__customer=user, orders__order_date=dt.now()
        )
        summa = sum(dish.price for dish in on_dishes)
        if not user.overdraft and summa > user.balance:
            context['balance'] = False
            return render(request, template, context)
        orders = [
            Order(
                dish=dish, customer=user, order_date=date.today()
            ) for dish in on_dishes
        ]
        Order.objects.bulk_create(orders)
        user.balance = user.balance - summa
        user.save()
        return redirect('dishes:profile', user.id)

    return redirect('dishes:index')
