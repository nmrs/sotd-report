import copy
import re
from collections import OrderedDict
from functools import lru_cache, cached_property
from pprint import pprint

from sotd_collator.base_alternate_namer import BaseAlternateNamer


class BrushAlternateNamer(BaseAlternateNamer):
    """
    Amalgamate names
    """

    bads = '(hmw|high.*mo|(2|3)band|shd|badger|silvertip|gelo|bulb|fan|finest|best|two\s*band)'
    boars = '(boar)'
    syns = '(timb|tux|mew|silk|synt|synbad|2bed|captain|cashmere|faux.*horse|black.*mag|g4)'

    __raw = OrderedDict({
        'DG B1': ['B1'],
        'DG B2': ['B2'],
        'DG B3': ['B3'],
        'DG B4': ['B4'],
        'DG B5': ['B5'],
        'DG B6': ['B6'],
        'DG B7': ['B7'],
        'DG B8': ['B8'],
        'DG B9A': ['B9A', 'b9.*alpha'],
        'DG B9B': ['B9B', 'b9.*bravo'],
        'Razorock Synthetic': ['Razorr*ock', '(^|\s)rr\s'],
        'Paladin': ['paladin'],
        'Stirling Synthetic': ['stirl.*kong'],
    })

    standard_makers = {
        'AP Shave Co': {'patterns': ['AP\s*shav'], 'default': 'Synthetic'},
        'Black Anvil': {'patterns': ['black.*anv'], 'default': 'Badger'},
        'Craving Shaving': {'patterns': ['crav.*shav'], 'default': 'Synthetic'},
        'Crescent City Craftsman': {'patterns': ['cres.*city'], 'default': 'Synthetic'},
        'DSCosmetics': {'patterns': ['DSCosmetics', 'DSC'], 'default': 'Synthetic'},
        'Dogwood': {'patterns': ['dogw'], 'default': 'Badger'},
        'Elite': {'patterns': ['elite'], 'default': 'Badger'},
        'Fendrihan': {'patterns': ['fendri'], 'default': 'Badger'},
        'Frank Shaving': {'patterns': ['frank.*sha'], 'default': 'Synthetic'},
        'Grizzly Bay': {'patterns': ['griz.*bay'], 'default': 'Badger'},
        'Heritage Collection': {'patterns': ['heritage'], 'default': 'Badger'},
        'Leonidam': {'patterns': ['leonidam'], 'default': 'Badger'},
        'Maggard': {'patterns': ['maggard'], 'default': 'Synthetic'},
        'Maseto': {'patterns': ['maseto'], 'default': 'Badger'},
        'Mozingo': {'patterns': ['mozingo'], 'default': 'Badger'},
        'Muhle': {'patterns': ['muhle'], 'default': 'Badger'},
        'Noble Otter': {'patterns': ['noble'], 'default': 'Badger'},
        'Oumo': {'patterns': ['oumo'], 'default': 'Badger'},
        'Oz Shaving': {'patterns': ['oz.*sha'], 'default': 'Synthetic'},
        'PAA': {'patterns': ['paa'], 'default': 'Synthetic'},
        'Prometheus Handcrafts': {'patterns': ['promethe'], 'default': 'Synthetic'},
        'Sawdust Creation Studios': {'patterns': ['sawdust'], 'default': 'Synthetic'},
        'Semogue Owners Club': {'patterns': ['SOC', 'sem.*owner.*club'], 'default': 'Boar'},
        'Simpson': {'patterns': ['simpson'], 'default': 'Badger'},
        'Spiffo': {'patterns': ['spiffo'], 'default': 'Badger'},
        'Stirling': {'patterns': ['stirl'], 'default': 'Badger'},
        'Teton Shaves': {'patterns': ['teton'], 'default': 'Badger'},
        'The Golden Nib': {'patterns': ['tgn', 'golden.*nib'], 'default': 'Boar'},
        'That Darn Rob': {'patterns': ['darn.*rob', 'tdr'], 'default': 'Badger'},
        'Viking': {'patterns': ['viking'], 'default': 'Badger'},
        'Vintage Blades': {'patterns': ['vintage.*blades'], 'default': 'Badger'},
        'WCS': {'patterns': ['wcs'], 'default': 'Synthetic'},
        'Whipped Dog': {'patterns': ['whipped.*dog'], 'default': 'Badger'},
        'Wild West Brushworks': {'patterns': ['wild.*west', 'wwb', 'ww.*brushw'], 'default': 'Synthetic'},
        'Yaqi': {'patterns': ['yaqi'], 'default': 'Synthetic'},
        'Zenith': {'patterns': ['zenith'], 'default': 'Boar'},
    }

    standard_fixup = {
            '{0} Badger': bads,
            '{0} Boar': boars,
            '{0} Synthetic': syns,
            # default to maker default
            '{0} {1}': '',

    }

    @cached_property
    def _raw(self):
        raw = copy.deepcopy(self.__raw)
        # for most makers just split them out into badger, boar and synthetic knots
        for maker, data in self.standard_makers.items():
            for regexp in data['patterns']:
                for maker_name_template, pattern in self.standard_fixup.items():
                    maker_name = maker_name_template.format(maker, data['default'])
                    if maker_name in raw:
                        raw[maker_name].append(regexp + '.*' + pattern)
                    else:
                        raw[maker_name] = [regexp + '.*' + pattern]
        return raw

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