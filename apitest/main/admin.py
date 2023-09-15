from django.contrib import admin
from main.models import *

@admin.register(Categories) 
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(Users) 
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'token', 'category')
    list_select_related = ('category',)
    
@admin.register(Orders) 
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    list_select_related = ('category',)
