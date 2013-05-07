import warnings

import requests


class WordLookup(object):

    BASE_URL = "http://words.bighugelabs.com/api/2/{api_key}/{word}/json"

    def __init__(self, settings, word):
        self.word = word
        try:
            self._api_key = settings["API_KEY"]
        except KeyError:
            raise Exception("Please set the value of the API_KEY setting")

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


class Library(object):

    def __init__(self, settings):
        self.settings = settings

    def _find_related_word(self, word, operator):
        lookup = WordLookup(self.settings, word)
        return list(lookup.get_data(operator))

    def find_synonyms(self, word):
        for word_type, word_list in self._find_related_word(word, "syn"):
            for word in word_list:
                yield word_type, word
