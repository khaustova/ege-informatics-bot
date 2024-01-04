### 1. О боте ###
Telegram-бот [Василий Питонов](https://t.me/vaspytbot) для подготовки к ЕГЭ по информатике представляет собой тренажёр заданий с 
выбором ответа и с кратким ответом, взятых из [Открытого банка тестовых заданий](https://ege.fipi.ru/bank).

:small_blue_diamond: Выбор раздела заданий  
:small_blue_diamond: Бесконечный режим из случайных заданий  
:small_blue_diamond: Просмотр статистики по каждому из разделов  
:small_blue_diamond: Возможность сброса прогресса по решенным разделам  
:small_blue_diamond: Панель администратора для управления заданиями 
и результатами в виде веб-приложения   
:small_blue_diamond: HTML-редактор текста задания с учётом тегов, поддерживаемых Telegram

### 2. Основные технологии ###
:small_orange_diamond: Python 3.11.4  
:small_orange_diamond: Aiogram 3.2.0  
:small_orange_diamond: Django 5.0  
:small_orange_diamond: Redis 7.0.5   
:small_orange_diamond: PostgreSQL 15.3
### 3. Запуск ###
1. Клонировать репозиторий:
```
git clone https://github.com/khaustova/ege-informatics-bot.git
```
2. Если бот ещё не создан, то в Telegram найти BotFather, с помощью команды **/newbot** создать нового бота и сохранить токен. 
3. Вставить токен в файл с настройками среды окружения **.env.example**, при необходимости, внести в него другие изменения и переименовать его в **.env**.  
4. Запустить проект с помощью докера:
```
docker-compose up --build
```
Веб-приложение с панелью администратора запустится на http://127.0.0.1:8000, сам бот будет доступен в Telegram.

