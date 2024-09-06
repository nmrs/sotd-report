import re
from functools import cached_property
from sotd_collator.base_name_extractor import BaseNameExtractor


class BrushNameExtractor(BaseNameExtractor):
    """
    From a given comment, extract the razor name
    """

    # patterns people use repeatedly to document the brush they used
    # but that we can't match to anything
    GARBAGE = ["Splash of warm water"]

    def _garbage(self):
        return self.GARBAGE

    @cached_property
    def detect_regexps(self):
        brush_name_re = r"""\w\t ./\-_()#;&\'\"|<>:$~+"""

        return [
            # self.sgrddy_detector("Brush"),
            self.imgur_detector("Brush"),
            self.tts_detector("Brush"),
        ]

    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        if "brush" in comment:
            return comment["brush"]

        return super().get_name(comment)

        # comment_text = self._to_ascii(comment["body"])
        # for detector in self.detect_regexps:
        #     res = detector.search(comment_text)

        #     # catch case where some jerk writes ❧ Brush Notes or similar
        #     # at some point this can be genericised in to a
        #     # block words / phrases list to catch razorock too
        #     if res and res.group(1) == "Notes":
        #         continue

        #     if res:
        #         result = res.group(1).strip()
        #         if len(result) > 0:
        #             # for pattern in self._garbage:
        #             #     if re.search(pattern, result, re.IGNORECASE):
        #             #         return None
        #             return result

        # # principal_name = self.alternative_namer.get_principal_name(comment_text)
        # # if principal_name == 'Semogue 2022':
        # #     print(comment_text)
        # #     print(res.group(1))

        # # if principal_name:
        # #     return principal_name

        # return None
