import re
from collections import OrderedDict
from functools import lru_cache

from sotd_collator.base_alternate_namer import BaseAlternateNamer


class BrushAlternateNamer(BaseAlternateNamer):
    """
    Amalgamate names
    """

    bads = '(hmw|high.*mo|(2|3)band|shd|badger|silvertip|gelo|bulb|fan|finest|best|two\s*band)'
    boars = '(boar)'
    syns = '(timb|tux|mew|silk|synt|synbad|2bed|captain|cashmere|faux.*horse|black.*mag)'

    _raw = OrderedDict({
        'DG B1': ['B1'],
        'DG B2': ['B2'],
        'DG B3': ['B3'],
        'DG B4': ['B4'],
        'DG B5': ['B5'],
        'DG B6': ['B6'],
        'DG B7': ['B7'],
        'DG B8': ['B8'],
        'DG B9A': ['B9A'],
        'DG B9B': ['B9B'],
        'Razorock Synthetic': ['Razorr*ock', '(^|\s)rr\s'],
        'Paladin': ['paladin'],
        'Stirling Synthetic': ['stirl.*kong'],
    })

    standard_makers = {
        'AP Shave Co': ['AP\s*shav'],
        'Black Anvil': ['black.*anv'],
        'Craving Shaving': ['crav.*shave'],
        'DSCosmetics': ['DSCosmetics', 'DSC'],
        'Dogwood': ['dogw'],
        'Frank Shaving': ['frank.*sha'],
        'Grizzly Bay': ['griz.*bay'],
        'Leonidam': ['leonidam'],
        'Maggard': ['maggard'],
        'Noble Otter': ['noble'],
        'Oz Shaving': ['oz.*sha'],
        'Prometheus Handcrafts': ['promethe'],
        'Simpson': ['simpson'],
        'Stirling': ['stirl'],
        'That Darn Rob': ['darn.*rob', 'tdr'],
        'WCS': ['wcs'],
        'Whipped Dog': ['whipped.*dog'],
        'Wild West Brushworks': ['wild.*west', 'wwb', 'ww.*brushw'],
        'Yaqi': ['yaqi'],
    }

    standard_fixup = {
            '{0} Badger': bads,
            '{0} Boar': boars,
            '{0} Synthetic': syns,

    }

    def __init__(self):
        # for most makers just split them out into badger, boar and synthetic knots
        for maker, regexps in self.standard_makers.items():
            for regexp in regexps:
                for maker_name_template, pattern in self.standard_fixup.items():
                    maker_name = maker_name_template.format(maker)
                    if maker_name in self._raw:
                        self._raw[maker_name].append(regexp + '.*' + pattern)
                    else:
                        self._raw[maker_name] = [regexp + '.*' + pattern]
                    self._raw[maker_name].append(pattern + '.*' + regexp)


    @lru_cache(maxsize=1024)
    def get_principal_name(self, name):
        # Standardise omega / semogues - dont want to list out every model number above,
        # but coerce them into a standard format
        name = name.lower().replace('semouge', 'semogue')

        omse_brand = re.search('(omega|semogue)', name, re.IGNORECASE)
        omse_model_num = re.search('[A-Za-z]*\d{3,}', name)
        if omse_brand and omse_model_num:
            return '{0} {1}'.format(
                omse_brand.group(1).title(),
                omse_model_num.group(0)
            )

        for alt_name_re in sorted(self._mapper.keys(), key=len, reverse=True):
            if re.search(alt_name_re, name, re.IGNORECASE):
                return self._mapper[alt_name_re]
        return None