"""Функции, выполняющие сопутствующие действия.
"""
import datetime as dt
from dishes import models as dishmodels


def end_time_accept_order():
    """Получает время окончания приёма заказов.

    Возвращает значение в часах типа int.
    большее, чем часов в сутках.
    Предполагается наличие в БД одного объекта хранящего ограничения.
    Если объектов больше одного, то использоваться будет первый,
    если объекта нет, то вернётся число большее, чем количество часов в сутках.

    Returns:
        int: `<25`, если ограничени установлены, `25`, если нет.
    """
    order_time = dishmodels.OrderTime.objects.filter(id__gt=0)
    if order_time:
        order_time = order_time[0]
        return order_time.get_end_time_hour
    return 25


def start_day_accept_order():
    """
    Получает день недели (0 - 7) с которого разрешён приём заказов.

    Переносит разрешаемый день на 1 один день вперёд,
    если текущее время больше, чем разрешённое для совершения заказа.

    Returns:
        int: `0 - 7`, то есть от понедельника до следующего понедельника.
    """
    start_day = dt.datetime.now().weekday() + int(
        dt.datetime.now().hour > end_time_accept_order()
    )
    return start_day


def get_delivery_date(delivery_week_day):
    """
    Получает дату доставки.

    Высчитывает календарную дату доставки исходя из переданного дня недели.
    
    Args:
        delivery_week_day (int):
            Число от 0 до 6 указываэщее день недели, как в datetime.

    Returns:
        obj (datetime): Календарная дата доставки.
    """
    delta = dt.timedelta((delivery_week_day) - 1 - dt.datetime.now().weekday())
    delivery_date = (dt.datetime.now() + delta).date()
    return delivery_date
