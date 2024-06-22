from datetime import datetime
from functools import lru_cache
import re
from unittest import TestCase

from numpy import equal
from blade_name_extractor import BladeNameExtractor

from sotd_collator.base_name_extractor import BaseNameExtractor


class BaseStagedNameExtractor(BaseNameExtractor):

    def detect_regexps(self):
        return []

    def _garbage(self):
        return []


class StagedRazorNameExtractor(BaseStagedNameExtractor):

    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        return comment["razor"] if "razor" in comment else None


class StagedBladeNameExtractor(BaseStagedNameExtractor):
    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        return comment["blade"] if "blade" in comment else None


class StagedBrushNameExtractor(BaseStagedNameExtractor):
    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        return comment["brush"] if "brush" in comment else None


class StagedUserNameExtractor(BaseStagedNameExtractor):
    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        return f'u/{comment["author"]}' if "author" in comment else None
        # return comment["created_utc"][0:10]


class StagedBladeUseExtractor(StagedBladeNameExtractor):

    def get_name(self, comment):
        name = super().get_name(comment)
        if name:
            reverse = name[::-1]
            pattern = r"[\)\]}]x?(\d+)[\(\[{]"
            match = re.search(pattern, reverse)

            if match:
                s = match.group(1)[::-1]
                return s

        return None


class StagedSoapNameExtractor(BaseStagedNameExtractor):
    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        return comment["soap"] if "soap" in comment else None


class TestStagedBladeUseExtractor(TestCase):

    cases = [
        {
            "str": "[365](https://www.reddit.com/r/Wetshavers_India/s/wSjU38Lgvg) (12x)",
            "expected result": 12,
        },
    ]


if __name__ == "__main__":
    sbue = TestStagedBladeUseExtractor()
    for case in sbue.cases:
        res = StagedBladeUseExtractor.extract_blade_use(case["str"])
        sbue.assertEqual(res, case["expected result"])
