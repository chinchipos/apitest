from django.db import models
import random
import string

class Categories(models.Model):
    name = models.CharField(
        'Название',
        max_length = 200,
        unique = True
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    def __str__(self):
        return self.name
    
class Users(models.Model):

    username = models.CharField(
        'Имя пользователя',
        max_length = 100,
        unique = True
    )

    email = models.EmailField(
        'email',
        max_length = 200,
        unique = True
    )

    password = models.CharField(
        'Пароль',
        max_length = 100
    )
    
    token = models.CharField(
        'Токен',
        max_length = 256,
        unique = True,
        blank = True,
        null = True,
        default = None
    )
    
    category = models.ForeignKey(
        Categories,
        verbose_name = 'Категория анкеты',
        on_delete = models.SET_NULL,
        blank = True,
        null = True,
        default = None
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
        
    def __str__(self):
        return self.username
        
    def create_token(self):
        characters = string.ascii_letters + string.digits
        self.token = ''.join(random.choice(characters) for i in range(256))
        self.save()
        return self.token
        
class Orders(models.Model):

    name = models.CharField(
        'Название',
        max_length = 200
    )
    
    category = models.ForeignKey(
        Categories,
        verbose_name = 'Категория заказа',
        on_delete = models.SET_NULL,
        blank = True,
        null = True,
        default = None
    )

    description = models.TextField(
        'Описание'
    )
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['name']
        
    def __str__(self):
        return self.name
