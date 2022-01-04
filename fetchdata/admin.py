from django.contrib import admin
from .models import ScraperData

# Register your models here.

@admin.register(ScraperData)
class ScraperDataAdmin(admin.ModelAdmin):
    list_display = ['cryptocurrency', 'ticker', 'yesterday_total', 'today_total', 'difference', 'yesterday_icospeaks', 'today_icospeaks', 'yesterday_cryptocom', 'today_cryptocom', 'yesterday_coinmarket', 'today_coinmarket', 'date']

