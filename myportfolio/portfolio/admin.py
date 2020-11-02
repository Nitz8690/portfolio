# from django_mongoengine import mongo_admin as admin

from django.contrib import admin

from .models import *

# Register your models here.


# class EmployeeAdmin(admin.DocumentAdmin):
#     model = Employee
#     fields = ('name', 'username')

admin.site.register(Project)
