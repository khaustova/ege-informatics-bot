from django.db import models
from dashboard.fields import MEditorField


class User(models.Model):
    user_id = models.PositiveBigIntegerField(
        primary_key=True, 
        verbose_name='Telegram ID'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Создан'
    )
    username = models.CharField(
        max_length=32, 
        null=True, 
        blank=True,
        verbose_name='Username'
    )
    first_name = models.CharField(
        max_length=256,
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
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.user_id}'
    
    
class Category(models.Model):
    category = models.CharField(
        max_length=256, 
        verbose_name='Категория'
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.category
    

class Assignment(models.Model):
    class QuestionTypes(models.TextChoices):
        SELECT_ONE = 'select_one', 'Выбор ответа'
        SHORT_REPLY = 'short_reply', 'Краткий ответ'   
    
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Категория'
    )
    question = MEditorField(verbose_name='Вопрос')
    question_type = models.CharField(
        max_length=64,
        choices=QuestionTypes.choices,
        verbose_name='Тип вопроса'
    )
    correct_answer = models.CharField(
        max_length=1024, 
        verbose_name='Правильный ответ'
    )
    choice_1 = models.CharField(
        max_length=1024, 
        blank=True,
        null=True,
        verbose_name='Неправильный ответ 1'
    )
    choice_2 = models.CharField(
        max_length=1024, 
        blank=True,
        null=True,
        verbose_name='Неправильный ответ 2'
    )
    choice_3 = models.CharField(
        max_length=1024, 
        blank=True,
        null=True,
        verbose_name='Неправильный ответ 3'
    )
    image = models.ImageField(
        upload_to ='images/',
        blank=True,
        null=True,
        verbose_name='Изображение')
    
    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
    
    def __str__(self):
        return f'{self.question[:128]}'
    
    
class Results(models.Model):
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        verbose_name='Пользователь'
    )
    question = models.ForeignKey(
        'Assignment', 
        on_delete=models.CASCADE, 
        verbose_name='Задание'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата решения'
    )
    status = models.BooleanField(verbose_name='Правильный ответ')
    
    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
    
    def __str__(self):
        status = 'правильно' if self.status else 'неправильно'
        return f'{self.user}: {self.question} - {status}'
