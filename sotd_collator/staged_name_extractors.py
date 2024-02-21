from datetime import datetime
from functools import lru_cache
import re
from blade_name_extractor import BladeNameExtractor

from sotd_collator.base_name_extractor import BaseNameExtractor


class BaseStagedNameExtractor(BaseNameExtractor):

    def detect_regexps(self):
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


class StagedBladeUseExtractor(BaseStagedNameExtractor):
    def extract_blade_use(self, input_string):
        pattern = r"\((\d+)\)|\[(\d+)\]|\{(\d+)\}"
        match = re.search(pattern, input_string)

        if match:
            return int(match.group(1) or match.group(2) or match.group(3))
        else:
            return None
