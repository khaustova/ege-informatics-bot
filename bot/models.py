from django.db import models


class User(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Создан'
    )
    user_id = models.PositiveBigIntegerField(
        primary_key=True, 
        verbose_name='Telegram ID'
    )
    username = models.CharField(
        max_length=32, 
        null=True, 
        blank=True,
        verbose_name='Username'
    )
    first_name = models.CharField(
        max_length=256,
        null=True, 
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=256,
        null=True, 
        blank=True,
        verbose_name='Фамилия'
    )
    
    is_admin = models.BooleanField(
        default=False,
        verbose_name='Права администратора'
    )
    is_blocked_bot = models.BooleanField(
        default=False,
        verbose_name='Бот заблокирован'
    )
    
    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.user_id}'