from django.test import TestCase
from main.models import *
from django.test import Client
import json

class MainTestCase(TestCase):
    def setUp(self):
        self.categoty1 = Categories.objects.create(name = "Категория1")
        self.categoty2 = Categories.objects.create(name = "Категория2")
    
    def user_registration(self, username, email, password, category):
        c = Client()
        
        response = c.post(f"/api/reg?username={username}&email={email}&password={password}&category={category}")
        print(response.status_code)
        data = json.loads(response.content)
        print(data['token'])
        
        return data['token']
        
    def test_user_registration(self):
        token = self.user_registration(username = 'Пользователь1', email = 'user1@test.ru', password = '12345678', category = self.categoty1.name)
        flag = True if len(token) == 256 else False
        self.assertEqual(flag, True)
    
    def test_order_creation(self):
        c = Client()
        
        token = self.user_registration(username = 'Пользователь2', email = 'user2@test.ru', password = '12345678', category = self.categoty2.name)
        
        response = c.post(f"/api/make_order?name=Заказ1&category={self.categoty1.name}&description=Заказ1&token={token}")
        print(response.status_code)
        data = json.loads(response.content)
        print(data)
        self.assertEqual(data['success'], True)

    def test_list_orders(self):
        user3 = Users.objects.create(
            username = "Пользователь3",
            email = "user3@test.ru",
            password = "12345678",
            token = "12345678",
            category = self.categoty1
        )
        print("Test USER3 has created.")
        
        Order3 = Orders.objects.create(
            name = "Заказ3",
            category = self.categoty1,
            description = "Заказ3"
        )
        print("Test ORDER3 has created.")
        
        c = Client()
        response = c.get("/api/list_orders?token=12345678")
        data = json.loads(response.content)
        print(response.status_code)
        print(data)
        
        self.assertEqual(data['success'], True)