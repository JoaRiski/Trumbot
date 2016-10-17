from django.conf import settings
from django.core.management.base import BaseCommand

from trumbot.models import Tweet

import markovify
import os


class Command(BaseCommand):
    help = "Generate a new markov chain database"

    def handle(self, *args, **options):
        self._create_database(settings.MARKOV_SAVE_LOCATION)

    def _create_database(self, location):
        tweets = Tweet.objects.all()

        print("Creating database...")
        sample = "\n".join([tweet.text for tweet in tweets])
        markov = markovify.NewlineText(sample)

        print("%d entries added!" % tweets.count())

        print("Generating 5 samples...")
        print("#" * 20)
        for i in range(5):
            print(markov.make_sentence())
        print("#" * 20)

        print("Saving database...")
        if not self._ensure_empty(location):
            print("Could not save database :(")
            return
        json = markov.chain.to_json()
        with open(location, "w") as f:
            f.write(json)
        print("Database saved to %s" % location)

    def _ensure_empty(self, location):
        if os.path.exists(location):
            if os.path.isfile(location):
                os.remove(location)
                print("Removed existing file at %s" % location)
                return True
            else:
                return False
        return True
