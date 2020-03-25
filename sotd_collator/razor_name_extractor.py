import unicodedata
import re
from sotd_post_locator import SotdPostLocator
from alternate_razor_names import AlternateRazorNames


class RazorNameExtractor(object):
    """
    For a given comment, extract the razor name, or fail
    """
    razor_name_re = r"""\w\t ./\-_()#;&\'\"|<>:$~"""

    detect_regexps = [
        re.compile(r'^[*\s\-+/]*Razor\s*[:*\-\\+\s/]+\s*([{0}]+)(?:\+|,|\n|$)'.format(razor_name_re),re.MULTILINE | re.IGNORECASE), # TTS and similar
        re.compile(r'\*Razor\*:.*\*\*([{0}]+)\*\*'.format(razor_name_re), re.MULTILINE | re.IGNORECASE), # sgrddy
        re.compile(r'^\*\*Safety Razor\*\*\s*-\s*([{0}]+)[+,\n]'.format(razor_name_re), re.MULTILINE | re.IGNORECASE),# **Safety Razor** - RazoRock - Gamechanger 0.84P   variant
        # re.compile(r'\*\s+[{0}]+\*\s+([{0}]+)\*\s+[{0}]+\*\s+[{0}]+\*\s+[{0}]+'.format("""\w\s./\-_()#;&\'\"+"""), re.MULTILINE),  # ntownuser *eyeroll*

    ]

    def __init__(self):
        self.arn = AlternateRazorNames()

    @staticmethod
    def _to_ascii(str_val):
        if str_val is None:
            return None
        else:
            return unicodedata.normalize('NFKD', str_val).encode('ascii', 'ignore').strip().decode('ascii')

    def get_razor_name(self, comment_text):
        comment_text = self._to_ascii(comment_text)
        # if 'favourite scents of all time is her morning' in comment_text:
        #     raise StopIteration(comment_text)
        for detector in self.detect_regexps:
            res = detector.search(comment_text)
            # catch case where we match against razorock
            if res and not (len(res.group(1)) >= 3 and res.group(1)[0:3] == 'ock'):
                return res.group(1).strip()

        principal_name = self.arn.get_principal_name(comment_text)
        if principal_name:
            return principal_name

        return None
