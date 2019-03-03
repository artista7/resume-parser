from spellchecker import SpellChecker as Checker
from pylanguagetool import init_config, api, print_errors


# class SpellChecker():
#     """
#         Module for spell checking functionalities
#     """
#     def __init__(self):
#         self.checker = Checker()
#
#     def check_misspelled(self, tokens, ignore_nps=False):
#         """
#             Given a list of words/tokens return the ones which are misspelled.
#         """
#         if ignore_nps:
#             tokens = [i[0] for i in pos_tag(tokens) if i[1][:2] != "NN"]
#         unknown_words = self.checker.unknown(tokens)
#         return unknown_words
#
#     def suggest(self, token):
#         """
#             Given a misspelled word suggest correct words
#         """
#         return self.checker.candidates(token)

CONFIG = {'verbose': False, 'api_url': 'https://languagetool.org/api/v2/',
            'no_color': False, 'clipboard': False, 'single_line': False,
            'input_type': 'txt', 'input file': None, 'lang': 'auto',
            'mother_tongue': None, 'preferred_variants': None,
            'enabled_rules': None, 'disabled_rules': None,
            'enabled_categories': None, 'disabled_categories': None,
            'enabled_only': False}
            
class SpellChecker():
    """
        Module for spell checking functionalities
    """
    def __init__(self):
        self.config = CONFIG

    def check_misspelled(self, text):
        """
            Given a list of words/tokens return the ones which are misspelled.
        """
        response = api.check(text, **self.config)
        matches = response["matches"]
        return matches

    def suggest(self, token):
        """
            Given a misspelled word suggest correct words
        """
        pass
