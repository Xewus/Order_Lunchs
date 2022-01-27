from django.contrib import admin
from django.urls import include, path


urlpatterns = (
    path('admin/', admin.site.urls),
    path('auth/', include('employees.urls', namespace='employees')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('dishes.urls', namespace='dishes')),
)
