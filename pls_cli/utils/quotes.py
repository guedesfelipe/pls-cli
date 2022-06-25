import json
import os
import random


def get_rand_quote():
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    with open(
        os.path.join(__location__, 'quotes.json'), 'r', encoding='utf-8'
    ) as quotes_file:
        list_of_quotes = json.load(quotes_file)
    return random.choice(list_of_quotes)
