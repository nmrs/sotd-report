import re
from functools import cached_property
from blade_name_extractor import BladeNameExtractor


class BladeUsageExtractor(BladeNameExtractor):
    """
    From a given comment, extract the blade usage
    """

    # patterns people use repeatedly to document the brush they used
    # but that we can't match to anything
    GARBAGE = []

    def get_name(self, comment):
        if "blade usage" in comment:
            return int(comment["blade usage"])

        name = super().get_name(comment)
        if name:
            s = name[::-1]
            match = re.search("[\)\]}]x?(\d+)[\(\[{]", s, re.IGNORECASE)
            if match:
                uses = match.group(1)[::-1]
                if uses != name:
                    return int(uses)

        return None

        # comment_text = self._to_ascii(comment["body"])
        # for detector in self.detect_regexps:
        #     res = detector.search(comment_text)
        #     if res:
        #         result = str(res.group(1)).strip()
        #         if len(result) > 0:
        #             # for pattern in self._garbage:
        #             #     if re.search(pattern, result, re.IGNORECASE):
        #             #         return None
        #             if res.lastindex > 1:
        #                 use_count = res.group(2).strip()
        #                 if len(use_count) > 0:
        #                     return f"{result} ({use_count})"
        #             return result

        # principal_name = self.alternative_namer.get_principal_name(comment_text)
        # if principal_name:
        #     return principal_name

        # return None
