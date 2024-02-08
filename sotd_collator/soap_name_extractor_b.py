import re
from functools import cached_property
from sotd_collator.blade_alternate_namer import BladeAlternateNamer
from sotd_collator.base_name_extractor import BaseNameExtractor


class SoapNameExtractor(BaseNameExtractor):
    """
    From a given comment, extract the razor name
    """

    @cached_property
    def alternative_namer(self):
        return BladeAlternateNamer()

    @cached_property
    def detect_regexps(self):
        soap_name_re = r"\w\t ./\-_()\[\]#;&\'\"|<>:$~"
        labels = "(?:lather|soap(?:\s*(?:&|and|\+|\/)\s*splash)?)"
        # labels = "(?:soap\s*(?:and)\s*splash|soap)"
        # j4m11mj 
        return [
            re.compile(
                fr"^[*\s\-+/]*{labels}\s*[:*\-\\+\s/]+\s*([{soap_name_re}]+)(?:\+|\n|$)",
                re.MULTILINE | re.IGNORECASE,
            ),  # TTS and similar
            re.compile(
                fr"\*{labels}\*:.*\*\*([{soap_name_re}]+)\*\*",
                re.MULTILINE | re.IGNORECASE,
            ),  # sgrddy
            re.compile(
                fr"^[*\s\-+/]*{labels}\s*[:*\-\\+\s/]+\s*\[*([{soap_name_re}]+)(?:\+|\n|$|]\()",
                re.MULTILINE | re.IGNORECASE,
            ),  # TTS style with link to eg imgur
        ]

    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        if "soap" in comment:
            return comment["soap"]

        comment_text = self._to_ascii(comment["body"])
        for detector in self.detect_regexps:
            res = detector.search(comment_text)
            if res:
                s = str(res.group(1)).strip()
                if len(s) > 0:
                    return s

        # principal_name = self.alternative_namer.get_principal_name(comment_text)
        # if principal_name:
        #     return principal_name

        return None