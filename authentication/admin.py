# admin.py
from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_premium')  # Добавьте колонку с полем is_premium
    list_filter = ('is_premium',)  # Добавляем фильтрацию по премиум статусу

admin.site.register(Profile, ProfileAdmin)
