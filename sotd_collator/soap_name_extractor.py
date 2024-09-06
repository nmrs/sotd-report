import re
from functools import cached_property
from sotd_collator.base_name_extractor import BaseNameExtractor


class SoapNameExtractor(BaseNameExtractor):
    """
    From a given comment, extract the blade name
    """

    # patterns people use repeatedly to document the brush they used
    # but that we can't match to anything
    GARBAGE = ["air bud ruler", "^face", "sample mashup"]

    def _garbage(self):
        return self.GARBAGE

    @cached_property
    def detect_regexps(self):
        # blade_name_re = r"""\w\t ./\-_()#;&\'\"|<>:$~"""

        # prefix = r"[*\s\-+/]*blade\s*[:*\-\\+\s/]+\s*\""
        # sgrddy =

        # "l4fg7co"
        labels = (
            # r"(?:\blather\b|\bsoap\b)(?:\s*(&|and|\/|\\)\s*(splash|\bas\b))?(?! bowl)"
            r"(?:\blather\b|\bsoap\b)(?:\s*(?:and|&|\\|\/)\s*(?:splash|as))?(?! bowl)"
        )
        return [
            # self.sgrddy_detector("Blade"),
            self.imgur_detector(labels),
            self.tts_detector(labels),
        ]

    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        if "soap" in comment:
            return comment["soap"]

        if "author" in comment and comment["author"] == "AirBudRuler":
            return None

        return super().get_name(comment)
