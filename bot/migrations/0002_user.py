# Generated by Django 5.0 on 2023-12-11 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('user_id', models.PositiveBigIntegerField(primary_key=True, serialize=False, verbose_name='Telegram ID')),
                ('username', models.CharField(blank=True, max_length=32, null=True, verbose_name='Username')),
                ('first_name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Фамилия')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Права администратора')),
                ('is_blocked_bot', models.BooleanField(default=False, verbose_name='Блокировка бота')),
            ],
        ),
    ]