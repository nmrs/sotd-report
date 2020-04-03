from collections import OrderedDict
from sotd_collator.base_alternate_namer import BaseAlternateNamer


class BladeAlternateNamer(BaseAlternateNamer):
    """
    Amalgamate names
    """
    _raw = OrderedDict({
        '7 0\'Clock - Permasharp': ['clock.*perm'],
        '7 0\'Clock - Sharpedge (Yellow)': ['clock.*sharpe', 'clock.*yellow'],
        '7 0\'Clock - Super Platinum (Black)': ['clock.*pla', 'clock.*black'],
        '7 0\'Clock - Super Stainless (Green)': ['clock.*sta', 'clock.*green', 'clock'],
        'Astra SP (Green)': ['astra.*plat', 'astra.*green', 'astra.*sp', 'astra'],
        'Astra Stainless': ['astra.*sta', 'astra.*blue'],
        'Bic Chrome': ['bic.*(chr|pla)'],
        'Bolzano': ['b(o|a)lzano'],
        'Derby Extra': ['derb.*extra'],
        'Derby Extra Blue': ['derb.*blue'],
        'Derby Premium': ['derb.*prem'],
        'Feather (DE)': ['^feather$', 'feather.*hi.*st'],
        'GEM': ['gem'],
        'Gillette Nacet': ['nacet'],
        'Gillette Rubie': ['rubie'],
        'Gillette Silver Blue': ['gsb', 'Gill.*sil.*blue', 'silver.*blue'],
        'Kai (DE)': ['^kai$', 'kai.*sta'],
        'Ladas': ['lada'],
        'Lord Classic': ['lord.*cla'],
        'Lord Cool': ['lord.*cool'],
        'Permasharp': ['perma\s*-*sharp'],
        'Personna Platinum': ['personn'],
        'Personna Blue': ['personn*a.*blue'],
        'Polsilver': ['polsilver', 'polsiver'],
        'Rapira Platinum Lux': ['rapira'],
        'Rapira Swedish': ['rapira.*swe'],
        'Shark Chrome': ['shark.*chr'],
        'Shark Stainless': ['shark'],
        'Shark Platinum': ['shark.*pla'],
        'Wizamet': ['wizamet'],
        'Voskhod': ['vokshod', 'voskhod']
    })

