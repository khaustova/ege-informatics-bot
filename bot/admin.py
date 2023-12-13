from django.contrib import admin
from .models import User, Quiz


@admin.register(User)
class UsearAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'username',
        'is_admin',
        'is_blocked_bot',
        'created_at',
    )
    
admin.site.register(Quiz)