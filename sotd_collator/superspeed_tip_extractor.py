import re
from functools import cached_property
from sotd_collator import razor_name_extractor
from sotd_collator.razor_name_extractor import RazorNameExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.base_name_extractor import BaseNameExtractor


class SuperSpeedTipExtractor(RazorNameExtractor):
    """
    From a given comment, extract the razor name
    """

    @cached_property
    def __razor_name_extractor(self):
        return RazorNameExtractor()
    
    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        entity_name = self.__razor_name_extractor.get_name(comment)
        if entity_name is None:
            return None

        principal_name = self.alternative_namer.get_principal_name(entity_name)
        if principal_name != 'Gillette Superspeed':
            return None
        
        tips = {
            'Red': ['red'],
            'Blue': ['blue'],
            'Black': ['black'],
            'Flare': ['flare', 'flair'],
        }

        for k, v in tips.items():
            for pattern in v:
                if re.search(pattern, entity_name, re.IGNORECASE):
                    return f'{k} Tip'

        return 'Standard Tip'
        
