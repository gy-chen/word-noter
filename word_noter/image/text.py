import re

word_pattern = re.compile(r'([a-z]+)', re.IGNORECASE)


def find_all_words(text):
    """Find all words in text, ignore digits.

    :param text:
    :return: list of words
    """
    return word_pattern.findall(text)
