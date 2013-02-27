from .utils import WordLookup


def _find_related_word(word, operator):
    lookup = WordLookup(word)
    return list(lookup.get_data(operator))


def find_synonyms(word):
    for word_type, word_list in _find_related_word(word, "syn"):
        for word in word_list:
            yield word_type, word
