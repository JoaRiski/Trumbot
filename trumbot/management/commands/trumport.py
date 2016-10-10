from django.conf import settings
from django.core.management.base import BaseCommand

from trumbot.models import Tweet

import json
import oauth2


REQUEST_SETTINGS = {
    "user_id": "25073877",
    "include_rts": "false",
    "exclude_replies": "true",
    "trim_user": "true",
    "count": "200"
}

URL = "https://api.twitter.com/1.1/statuses/user_timeline.json?%s"
# count=200&trim_user=true&exclude_replies=false&include_rts=false&user_id=25073877"


def oauth_request(url):
    consumer = oauth2.Consumer(key=settings.TWITTER_CONSUMER_KEY, secret=settings.TWITTER_CONSUMER_SECRET)
    token = oauth2.Token(key=settings.TWITTER_TOKEN_KEY, secret=settings.TWITTER_TOKEN_SECRET)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method="GET")
    return content


class Command(BaseCommand):
    help = "Truport tweets"

    def _get_request(self, *args, **kwargs):
        arguments = []

        for key, value in kwargs.items():
            arguments.append("%s=%s" % (key, value))

        arguments = "&".join(arguments)

        return URL % arguments

    def handle(self, *args, **options):
        data = json.loads(oauth_request(self._get_request(**REQUEST_SETTINGS)).decode())

        created_count = 0
        total_count = len(data)
        for i, tweet in enumerate(data):
            print("Processing tweets %d / %d" % (i + 1, total_count))
            text = tweet["text"].replace("\\n", "\n")
            user = tweet["user"]["id"]
            pk = tweet["id"]
            tweet, created = Tweet.objects.get_or_create(text=text, user=user, pk=pk)
            if created:
                created_count += 1
        print("%d tweets created" % created_count)
