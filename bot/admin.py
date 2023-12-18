from django.contrib import admin
from .models import User, Category, Subcategory, Assignment, Results


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


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = (
        'subcategory',
    )

 
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'subcategory',
        'question'[:64],
        'question_type',
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