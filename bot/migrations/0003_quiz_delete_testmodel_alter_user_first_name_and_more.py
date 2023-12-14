# Generated by Django 5.0 on 2023-12-12 21:35

import mdeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', mdeditor.fields.MDTextField()),
            ],
        ),
        migrations.DeleteModel(
            name='TestModel',
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='a', max_length=256, verbose_name='Имя'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='is_blocked_bot',
            field=models.BooleanField(default=False, verbose_name='Бот заблокирован'),
        ),
    ]