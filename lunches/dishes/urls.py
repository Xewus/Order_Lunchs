from django.urls import path

from .views import index, list_dishes, profile

app_name = 'dishes'

urlpatterns = (
    path('', index, name='index'),
    path('list_dishes/<str:order_day>/', list_dishes, name='list_dishes'),
    path('profile/<int:id>/', profile, name='profile'),
    

)
