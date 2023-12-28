from django.contrib import admin
from .models import User, Category, Assignment, Results


@admin.register(User)
class UsearAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'username',
        'is_admin',
        'is_blocked_bot',
        'created_at',
    )
    
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category',
    )

 
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'category',
        'question'[:64],
        'correct_answer'[:64],
    )


@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'question'[:64],
        'status',
    )
    list_filter = ('user',)