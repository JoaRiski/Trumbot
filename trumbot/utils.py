from django.conf import settings

import markovify


def _load_markov(location):
    with open(location, "r") as f:
        chain_json = f.read()
    return markovify.Text.from_chain(chain_json=chain_json)


def generate_random_sentence():
    markov = _load_markov(settings.MARKOV_SAVE_LOCATION)
    return markov.make_sentence()
