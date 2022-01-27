from atexit import register

from django.contrib import admin

from .models import Department, Employer

register = admin.site.register

register(Department)
register(Employer)
