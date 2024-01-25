import re

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

class StagedUserNameExtractor(BaseNameExtractor):

    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        return f'u/{comment["author"]}' if "author" in comment else None

class StagedBladeUseExtractor(BaseNameExtractor):

    def extract_blade_use(self, input_string):
        pattern = r'\((\d+)\)|\[(\d+)\]|\{(\d+)\}'
        match = re.search(pattern, input_string)
        
        if match:
            return int(match.group(1) or match.group(2) or match.group(3))
        else:
            return None
    
    def get_name(self, comment):
        if "blade" not in comment: return None
        return self.extract_blade_use(comment["blade"])
        



