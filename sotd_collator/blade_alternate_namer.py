from collections import OrderedDict
from sotd_collator.base_alternate_namer import BaseAlternateNamer


class BladeAlternateNamer(BaseAlternateNamer):
    """
    Amalgamate names
    """
    _raw = OrderedDict({
        '7 O\'Clock - Permasharp': ['clock.*perm'],
        '7 O\'Clock - Sharpedge (Yellow)': ['clock.*sharpe', 'clock.*yellow'],
        '7 O\'Clock - Super Platinum (Black)': ['clock.*pla', 'clock.*black'],
        '7 O\'Clock - Super Stainless (Green)': ['clock.*sta', 'clock.*green', 'clock'],
        'Astra SP (Green)': ['astra.*plat', 'astra.*green', 'astra.*sp', 'astra'],
        'Astra Stainless': ['astra.*sta', 'astra.*blue'],
        'Bic Chrome': ['bic.*(chr|pla)'],
        'Bolzano': ['b(o|a)lzano'],
        'Derby Extra': ['derb.*extra'],
        'Derby Extra Blue': ['derb.*blue'],
        'Derby Premium': ['derb.*prem'],
        'Feather (DE)': ['^feather$', 'feather.*hi.*st', 'feather.*hs'],
        'Feather FHS-1': ['fhs-1'],
        'Feather Pro (AC)': ['feather.*pro'],
        'Feather Pro Light (AC)': ['feather.*light'],
        'Feather Pro Super (AC)': ['feather.*super', 'pro\s*super'],
        'Feather ProGuard (AC)': ['feather.*guard'],
        'Feather Soft Guard (AC)': ['feather.*soft'],
        'GEM': ['gem'],
        'Gillette Nacet': ['nacet'],
        'Gillette Rubie': ['rubie'],
        'Gillette Silver Blue': ['gsb', 'Gill.*sil.*blue', 'silver.*blue'],
        'Kai (DE)': ['^kai$', 'kai.*sta', 'kai.*ss'],
        'Kai Captain Blade (AC)': ['kai.*blade'],
        'Kai Captain Sharpblade (AC)': ['kai.*sharp'],
        'Kai Captain Titan Mild (AC)': ['kai.*titan'],
        'Kai Captain Titan Mild Protouch (AC)': ['kai.*touch'],
        'Ladas': ['lada'],
        'Lord Classic': ['lord.*cla'],
        'Lord Cool': ['lord.*cool'],
        'Permasharp': ['perma\s*-*sharp'],
        'Personna Platinum': ['personn'],
        'Personna Blue': ['personn*a.*blue'],
        'Polsilver': ['pol(i|-)*silver', 'polsiver'],
        'Rapira Platinum Lux': ['rapira'],
        'Rapira Swedish': ['rapira.*swe'],
        'Schick Proline': ['proline'],
        'Shark Chrome': ['shark.*chr'],
        'Shark Stainless': ['shark'],
        'Shark Platinum': ['shark.*pla'],
        'Wizamet': ['wizamet'],
        'Voskhod': ['vokshod', 'voskhod', 'voshk']
    })

