from collections import OrderedDict
from sotd_collator.base_alternate_namer import BaseAlternateNamer


class BladeAlternateNamer(BaseAlternateNamer):
    """
    Amalgamate names
    """
    _raw = OrderedDict({
        'Gillette Nacet': ['nacet'],
        'Gillette Silver Blue': ['gsb', 'Gill.*sil.*blue'],
        'Polsilver': ['polsilver'],
        'Wizamet': ['wizamet'],
        'Voskhod': ['vokshod', 'voskhod']
    })

