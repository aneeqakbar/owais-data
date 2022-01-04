from django.db import models

# Create your models here.

class ScraperData(models.Model):
    SCRAPER_NAMES = (
        ('T', 'Telegram'),
        ('R', 'Reddit'),
    )

    scraper_name = models.CharField(max_length=255, choices=SCRAPER_NAMES)
    cryptocurrency = models.CharField(max_length=255)
    ticker = models.CharField(max_length=50)
    yesterday_total = models.IntegerField(default=0, null=True)
    today_total = models.IntegerField(default=0, null=True)
    difference = models.IntegerField(default=0, null=True)
    yesterday_icospeaks = models.IntegerField(default=0, null=True)
    today_icospeaks = models.IntegerField(default=0, null=True)
    yesterday_cryptocom = models.IntegerField(default=0, null=True)
    today_cryptocom = models.IntegerField(default=0, null=True)
    yesterday_coinmarket = models.IntegerField(default=0, null=True)
    today_coinmarket = models.IntegerField(default=0, null=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)