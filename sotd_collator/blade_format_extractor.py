import re
from functools import cached_property
from sotd_collator.blade_alternate_namer import BladeAlternateNamer
from sotd_collator.base_name_extractor import BaseNameExtractor
from sotd_collator.blade_name_extractor import BladeNameExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.razor_name_extractor import RazorNameExtractor

class BladeFormatExtractor(BaseNameExtractor):
    """
    From a given comment, extract the blade type. Note doesnt differentiate between DE and Half DE razors because technical reasons
    """
    # we name any format that isnt DE in the blade name itself
    BLADE_FORMATS =['AC', 'GEM', 'Injector']


    NON_DE_RAZORS = {
        'Alumigoose': 'AC',
        'Asylum Evolution': 'AC',
        'ATT SE1': 'AC',
        'Blackland Sabre': 'GEM',
        'Blackland Vector': 'AC',
        'Boker Straight': 'Straight',
        'Cartridge / Disposable': 'Cart',
        'CJB Shavette': 'AC',
        'Cobra': 'AC',
        'Colonial General': 'AC',
        'Dovo Straight': 'Straight',
        'Enders Speed Shaver': 'Enders',
        'Ever Ready 1912': 'GEM',
        'Ever Ready 1914': 'GEM',
        'Ever Ready 1924': 'GEM',
        'Ever Ready Streamline': 'GEM',
        'Ever Ready E-Bar': 'GEM',
        'Ever Ready G-Bar': 'GEM',
        'Feather DX': 'AC',
        'Feather SS': 'AC',
        'Filarmonica Straight': 'Straight',
        'GEM 1912': 'GEM',
        'GEM Bullet Tip': 'GEM',
        'GEM Clog Pruf': 'GEM',
        'GEM Damaskeene': 'GEM',
        'GEM Featherweight': 'GEM',
        'GEM G-Bar': 'GEM',
        'GEM Junior': 'GEM',
        'GEM Micromatic Open Comb': 'GEM',
        'GEM Pushbutton': 'GEM',
        'Gillette Guard': 'Cart',
        'Headblade ATX': 'Cart',
        'J A Henckels Straight': 'Straight',
        'Kai Captain Folding': 'AC',
        'Kai Captain Kamisori': 'AC',
        'Kai Excelia Kamisori': 'AC',
        'Koraat Straight': 'Straight',
        'EldrormR Industries MM24': 'GEM',
        'Mongoose': 'AC',
        'Occams Razor Enoch': 'AC',
        'OneBlade Core': 'FHS',
        'OneBlade Genesis': 'FHS',
        'OneBlade Hybrid': 'FHS',
        'Other Straight Razor': 'Straight',
        'Paradigm SE': 'AC',
        'Portland Razor Co. Straight': 'Straight',
        'Ralf Aust Straight': 'Straight',
        'Razorock Hawk v1': 'AC',
        'Razorock Hawk v2': 'AC',
        'Razorock Hawk v3': 'AC',
        'Rolls Razor': 'Rolls',
        'Schick Hydromagic': 'Injector',
        'Schick Injector': 'Injector',
        'Schick BBR-1J Kamisori Shavette': 'AC',
        'Supply SE': 'Injector',
        'Wade & Butcher Straight': 'Straight',
        'Weck Sextoblade': 'Hair Shaper',
        'Weck 450-110': 'Hair Shaper',
        'Wolfman WR3': 'GEM',

    }

    razor_name_extractor = RazorNameExtractor()
    razor_alternate_namer = RazorAlternateNamer()
    blade_name_extractor = BladeNameExtractor()
    blade_alternate_namer = BladeAlternateNamer()


    def _get_format_from_blade_name(self, blade_name):
        for b_format in self.BLADE_FORMATS:
            if b_format in blade_name:
                return b_format


    @BaseNameExtractor.post_process_name
    def get_name(self, comment_text):
        comment_text = self._to_ascii(comment_text)
        blade_name = self.blade_name_extractor.get_name(comment_text)
        if blade_name:
            renamed_blade = self.blade_alternate_namer.get_principal_name(blade_name)
            blade_name = renamed_blade if renamed_blade else blade_name

            bf = self._get_format_from_blade_name(blade_name)
            if bf:
                return bf

        # fall back to using razor name
        razor_name = self.razor_name_extractor.get_name(comment_text)
        if razor_name:
            renamed_razor = self.razor_alternate_namer.get_principal_name(razor_name)
            razor_name = renamed_razor if renamed_razor else razor_name

            try:
                return self.NON_DE_RAZORS[razor_name]
            except KeyError:
                return 'DE'

        # default to DE. Possibly correct?
        return 'DE'


