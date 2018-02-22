from django.core.management.base import BaseCommand
from telegram_bot import telegrambot


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            telegrambot.main()
        except Exception as e:
            raise e
