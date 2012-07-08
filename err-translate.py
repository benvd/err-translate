from errbot.botplugin import BotPlugin
from errbot.jabberbot import botcmd

from urllib import urlencode
from urllib2 import Request, urlopen

import re


class Translate(BotPlugin):

    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'client': 't', 'sl': None, 'tl': None, 'text': None}
    url = 'http://translate.google.com/translate_a/t'

    languages = {
        'af': 'Afrikaans',
        'sq': 'Albanian',
        'ar': 'Arabic',
        'hy': 'Armenian',
        'az': 'Azerbaijani',
        'eu': 'Basque',
        'be': 'Belarusian',
        'bn': 'Bengali',
        'bg': 'Bulgarian',
        'ca': 'Catalan',
        'zh-CN': 'Chinese (Simplified)',
        'zh-TW': 'Chinese (Traditional)',
        'hr': 'Croatian',
        'cs': 'Czech',
        'da': 'Danish',
        'nl': 'Dutch',
        'en': 'English',
        'eo': 'Esperanto',
        'et': 'Estonian',
        'tl': 'Filipino',
        'fi': 'Finnish',
        'fr': 'French',
        'gl': 'Galician',
        'ka': 'Georgian',
        'de': 'German',
        'el': 'Greek',
        'gu': 'Gujarati',
        'ht': 'Haitian Creole',
        'he': 'Hebrew',
        'hi': 'Hindi',
        'hu': 'Hungarian',
        'is': 'Icelandic',
        'id': 'Indonesian',
        'ga': 'Irish',
        'it': 'Italian',
        'ja': 'Japanese',
        'kn': 'Kannada',
        'ko': 'Korean',
        'la': 'Latin',
        'lv': 'Latvian',
        'lt': 'Lithuanian',
        'mk': 'Macedonian',
        'ms': 'Malay',
        'mt': 'Maltese',
        'no': 'Norwegian',
        'fa': 'Persian',
        'pl': 'Polish',
        'pt': 'Portuguese',
        'ro': 'Romanian',
        'ru': 'Russian',
        'sr': 'Serbian',
        'sk': 'Slovak',
        'sl': 'Slovenian',
        'es': 'Spanish',
        'sw': 'Swahili',
        'sv': 'Swedish',
        'ta': 'Tamil',
        'te': 'Telugu',
        'th': 'Thai',
        'tr': 'Turkish',
        'uk': 'Ukrainian',
        'ur': 'Urdu',
        'vi': 'Vietnamese',
        'cy': 'Welsh',
        'yi': 'Yiddish'}

    @botcmd
    def translate(self, mess, args):
        """Translate a string from a certain source language to a target language.
        Example: !translate en fr computer"""
        arguments = self.get_arguments(args)

        if None in arguments:
            return 'Please specify at least a target language.'

        self.params['sl'], self.params['tl'], self.params['text'] = arguments

        request = Request(self.url, urlencode(self.params), self.headers)
        raw_response = urlopen(request).read()

        # The response we're getting from the API often has invalid syntax,
        # removing duplicate commas seems to fix it.
        response = eval(re.sub(r',,+', ',', raw_response))
        try:
            return response[0][0][0]
        except IndexError:
            return 'Failed to perform translation.'

    @botcmd
    def translate_langs(self, mess, args):
        """List all supported languages."""
        return '\n'.join(sorted(['%s (%s)' % (self.languages[key], key) for key in self.languages]))

    def get_arguments(self, args):
        words = args.strip().split()
        sl, tl, text = None, None, None

        if words[0] in self.languages:
            if words[1] in self.languages:
                sl = words[0]
                tl = words[1]
                text = ' '.join(words[2:])
            else:
                sl = 'auto'
                tl = words[0]
                text = ' '.join(words[1:])

        return (sl, tl, text)
