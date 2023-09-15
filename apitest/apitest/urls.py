"""
URL configuration for apitest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from ninja import Schema
from ninja.security import APIKeyQuery
from ninja.security import APIKeyHeader
from main.models import *

api = NinjaAPI(csrf = True)

#------------------------------  
class AuthCheck:
    def authenticate(self, request, key):
        if Users.objects.filter(token = key).exists():
            return Users.objects.get(token = key).token

class QueryKey(AuthCheck, APIKeyQuery):
    param_name = "token"
    pass

class HeaderKey(AuthCheck, APIKeyHeader):
    param_name = "token"
    pass

#------------------------------ 
# Регистрация пользователя
@api.post("/reg")
def users_registration(request, username: str, email: str, password: str, category: str):
    user, user_created = Users.objects.get_or_create(
        username = username,
        email = email,
        password = password
    )
    
    category, category_created = Categories.objects.get_or_create(name = category)
    if user.category != category:
        user.category = category
        user.save()
    
    return {"success": True, "token": user.create_token()} if user_created else {"success": True, "token": user.token}

#------------------------------
# Создание заказа
@api.post("/make_order", auth = [QueryKey(), HeaderKey()])
def create_order(request, name: str, category: str, description: str, token: str):
    if request.auth:
        order = Orders.objects.create(
            name = name,
            category = Categories.objects.get(name = category),
            description = description
        )
        return {"success": True, "order": order.pk}
    else:
        return {"success": False}

#------------------------------
# Получение списка релевантных заказов  
@api.get("/list_orders", auth = [QueryKey(), HeaderKey()])
def list_orders(request, token: str):
    if request.auth:
        user = Users.objects.get(token = token)
        orders = [{"id": order.pk, "name": order.name, "category": order.category.pk, "description": order.description} for order in Orders.objects.filter(category = user.category).select_related('category')]
        return {'success': True, "orders": orders}
    else:
        return {"success": False}
    
#------------------------------  
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
