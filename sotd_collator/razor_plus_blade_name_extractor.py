from sotd_collator.blade_name_extractor import BladeNameExtractor
from sotd_collator.razor_name_extractor import RazorNameExtractor
from sotd_collator.base_name_extractor import BaseNameExtractor


class RazorPlusBladeNameExtractor(object):
    """
    From a given comment, extract the combined razor + blade name
    """

    def __init__(self):
        self.bne = BladeNameExtractor()
        self.rne = RazorNameExtractor()

    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        razor_name = self.rne.get_name(comment)
        blade_name = self.bne.get_name(comment)

        if razor_name and blade_name:
            return f"{razor_name}\001{blade_name}"

        return None
