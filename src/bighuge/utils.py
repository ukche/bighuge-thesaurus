import warnings

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

import requests


class WordLookup(object):

    BASE_URL = "http://words.bighugelabs.com/api/2/{api_key}/{word}/json"

    def __init__(self, word):
        self.word = word
        try:
            self._api_key = settings.BIGHUGE_API_KEY
        except AttributeError:
            raise ImproperlyConfigured(
                "Please set the value of the BIGHUGE_API_KEY setting")

    @property
    def url(self):
        return self.BASE_URL.format(api_key=self._api_key, word=self.word)

    def _lookup_word(self):
        response = requests.get(self.url)
        response.raise_for_status()
        # TODO check that response is JSON?
        return response.json

    def get_data(self, operator):
        try:
            all_data = self._lookup_word()
        except requests.exceptions.HTTPError, e:
            if e.response.status_code == 404:
                # No related words found
                warnings.warn("%s not found in thesaurus" % self.word)
                return
            raise
        for word_type, data in all_data.iteritems():
            if operator in data:
                yield word_type, data[operator]
