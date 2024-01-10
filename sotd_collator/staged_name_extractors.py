import re
from functools import cached_property
from sotd_collator.base_alternate_namer import BaseAlternateNamer
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.base_name_extractor import BaseNameExtractor


class StagedRazorNameExtractor(BaseNameExtractor):

    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        return comment["razor"] if "razor" in comment else None

class StagedBladeNameExtractor(BaseNameExtractor):

    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        return comment["blade"] if "blade" in comment else None

class StagedBrushNameExtractor(BaseNameExtractor):

    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        return comment["brush"] if "brush" in comment else None

