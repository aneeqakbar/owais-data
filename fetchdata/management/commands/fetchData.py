from django.core.management.base import BaseCommand, CommandError
from fetchdata.cron import fetch_reddit_data, fetch_telegram_data

class Command(BaseCommand):
    help = 'Runs the cron job manually'

    def handle(self, *args, **options):
        fetch_telegram_data()
        fetch_reddit_data()
        self.stdout.write(self.style.SUCCESS('Successfully fetched data'))
