from collections import OrderedDict
from sotd_collator.base_alternate_namer import BaseAlternateNamer


class BrushAlternateNamer(BaseAlternateNamer):
    """
    Amalgamate names
    """

    bads = '(hmw|high.*mo|(2|3)band|shd|badger|silvertip|gelo|bulb|fan)'
    boars = '(boar)'
    syns = '(timb|tux|mew|silk|synt|synbad|2bed|captain)'

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
        'Razorock Synthetic': ['Razorr*ock', '(^|\s)rr\s']
    })

    standard_makers = {
        'AP Shave Co': ['AP\s*shav.*{0}'],
        'Black Anvil': ['black.*anv.*{0}'],
        'Craving Shaving': ['crav.*shave.*{0}'],
        'DSCosmetics': ['DSCosmetics.*{0}', 'DSC.*{0}'],
        'Dogwood': ['dogw.*{0}'],
        'Frank Shaving': ['frank.*sha.*{0}'],
        'Grizzly Bay': ['griz.*bay.*{0}'],
        'Leonidam': ['leonidam.*{0}'],
        'Maggard': ['maggard.*{0}'],
        'Noble Otter': ['noble.*{0}'],
        'Oz Shaving': ['oz.*sha.*{0}'],
        'Prometheus Handcrafts': ['promethe.*{0}'],
        'Stirling': ['stirl.*{0}'],
        'That Darn Rob': ['darn.*rob.*{0}', 'tdr.*{0}'],
        'WCS': ['wcs.*{0}'],
        'Whipped Dog': ['whipped.*dog.*{0}'],
        'Wild West Brushworks': ['wild.*west.*bru.*{0}', 'wwb.*{0}', 'ww.*brushw.*{0}'],
        'Yaqi': ['yaqi.*{0}'],
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
                        self._raw[maker_name].append(regexp.format(pattern))
                    else:
                        self._raw[maker_name] = [regexp.format(pattern)]


