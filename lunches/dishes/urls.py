from django.urls import path

from .views import index, list_dishes, profile, profile_orders

app_name = 'dishes'

urlpatterns = (
    path('', index, name='index'),
    path('list_dishes/<int:order_day>/', list_dishes, name='list_dishes'),
    path('profile/<int:id>/', profile, name='profile'),
    path('profile/<int:id>/orders/', profile_orders, name='profile_orders'),
    path('profile/<int:id>/orders/<int:order_id>', profile_orders, name='profile_order'),
    

)
