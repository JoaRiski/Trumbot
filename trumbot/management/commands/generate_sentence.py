from django.core.management.base import BaseCommand

from trumbot.utils import generate_random_sentence


class Command(BaseCommand):
    help = "Generate random sentence"

    def handle(self, *args, **options):
        print(generate_random_sentence())
