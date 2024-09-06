from gc import garbage
import re
from functools import cached_property
from tokenize import ContStr
from sotd_collator.base_name_extractor import BaseNameExtractor


class RazorNameExtractor(BaseNameExtractor):
    """
    From a given comment, extract the razor name
    """

    # patterns people use repeatedly to document the razor they used
    # but that we can't match to anything
    GARBAGE = []

    def _garbage(self):
        return self.GARBAGE

    RAZOR_NAME_RE = r"\w\t ./\-_()#;&\'\"|<>:$~"

    # def tts_detector(self, token):
    #     return re.compile(
    #         rf"^[*\s\-+/]*{token}\s*[:*\-\\+\s/]+\s*([{self.RAZOR_NAME_RE}]+)(?:\+|,|\n|$)",
    #         re.MULTILINE | re.IGNORECASE,
    #     )

    # @cached_property
    # def detect_regexps(self):

    #     return [
    #         # self.sgrddy_detector("Razor"),
    #         self.imgur_detector("(?:safety\s+)?razor(?!\s*blade)"),
    #         self.tts_detector("(?:safety\s+)?razor(?!\s*blade)"),
    #         self.imgur_detector("Blade\sHolder"),
    #         self.tts_detector("Blade\sHolder"),
    #     ]

    def detect_labels(self):

        return [
            "(?:safety\s+)?razor(?!\s*blade)",
            "Blade\sHolder",
        ]

    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        if "razor" in comment:
            return comment["razor"]

        comment_text = self._to_ascii(comment["body"])

        # deal with u/Enndeegee nonsense (e.g.https://www.reddit.com/r/Wetshaving/comments/1auh3xb/comment/kr5yhuf/)
        res = self.tts_detector("razor brand").search(comment_text)
        if res:
            brand = res.group(1).strip()
            res = res = self.tts_detector("razor model").search(comment_text)
            if res:
                model = res.group(1).strip()
                result = f"{brand} {model}".strip()
                if len(result) > 0:
                    return result

        # for detector in self.detect_regexps:
        #     res = detector.search(comment_text)
        #     # catch case where some jerk writes ❧ Razor and Blade Notes or similar
        #     # at some point this can be genericised
        #     # to a block words / phrases list to catch razorock too
        #     if res and "and blade note" in res.group(1).lower():
        #         return None

        return super().get_name(comment)
        # catch case where we match against razorock
        # if res and not (len(res.group(1)) >= 3 and res.group(1)[0:3] == "ock"):
        #     result = res.group(1).strip()
        #     if len(result) > 0:
        #         # for pattern in self._garbage:
        #         #     if re.search(pattern, result, re.IGNORECASE):
        #         #         return None
        #         return result

        # principal_name = self.alternative_namer.get_principal_name(comment_text)
        # if principal_name:
        #     return principal_name

        return None
