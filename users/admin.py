from django.contrib import admin
from .models import Profile, TelegramAccounts

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
    ]

@admin.register(TelegramAccounts)
class TelegramAccountsAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'hash_key',
        'hash_id',
        'number',
    ]