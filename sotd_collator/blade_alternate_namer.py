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
        '7 O\'Clock - Super Stainless (Green)': ['clock.*sta', 'clock.*green', 'clock', 'gil.*et.*super.*stain'],
        'Aeterna': ['aeter'],
        'Astra SP (Green)': ['astra.*plat', 'astra.*green', 'astra.*sp', 'astra'],
        'Astra Stainless': ['astra.*sta', 'astra.*blue'],
        'Bic Astor Stainless': ['bic.*(ast|stai)'],
        'Bic Chrome': ['bic.*(chr|pla)', 'bic'],
        'Big Ben': ['big ben'],
        'Bolzano': ['b(o|a)lzano'],
        'Crystal': ['crystal'],
        'Dorco BB-20 (AC)': ['dorco.*bb*'],
        'Dorco ST-300': ['dorco.*st.*300', 'dorco'],
        'Dorco ST-301': ['dorco.*st.*301'],
        'Dorco Titan': ['dorco.*titan'],
        'Derby Extra': ['derb.*extra', 'derby'],
        'Derby Extra Blue': ['derb.*blue'],
        'Derby Premium': ['derb.*prem'],
        'Eddison Stainless': ['eddison'],
        'Euromax': ['euromax'],
        'Feather (DE)': ['^feather$', 'feather.*hi.*st', 'feather.*hs', 'feather \s*blade'],
        'Feather FHS-1': ['fhs-1'],
        'Feather Pro (AC)': ['feather.*pro'],
        'Feather Pro Light (AC)': ['feather.*light'],
        'Feather Pro Super (AC)': ['feather.*super', 'pro\s*super'],
        'Feather ProGuard (AC)': ['feather.*guard'],
        'Feather Soft Guard (AC)': ['feather.*soft'],
        'GEM': ['gem'],
        'Gillette Nacet': ['nacet'],
        'Gillette Platinum': ['gil.*pla'],
        'Gillette Rubie': ['rubie'],
        'Gillette Silver Blue': ['gsb', 'Gill.*sil.*blue', 'silver.*blue'],
        'Gillette Spoiler': ['gil.*et.*spoil'],
        'Gillette Wilkinson Sword': ['gil.*et.*wilk.*swor'],
        'Kai (DE)': ['^kai$', 'kai.*sta', 'kai.*ss'],
        'Kai Captain Blade (AC)': ['kai.*blade', 'kai captain\s*$'],
        'Kai Captain Sharpblade (AC)': ['kai.*sharp'],
        'Kai Captain Titan Mild (AC)': ['kai.*titan'],
        'Kai Captain Titan Mild Protouch (AC)': ['kai.*touch'],
        'King C Gillette': ['king.*c.*gil.*et', 'gil.*et.*king.*c'],
        'Ladas': ['lada'],
        'Lord Classic': ['lord.*cla'],
        'Lord Cool': ['lord.*cool'],
        'Muhle': ['muhle'],
        'Permasharp': ['perma\s*-*sharp'],
        'Personna Platinum': ['personn.*plat', 'personn*a'],
        'Personna Med Prep': ['person.*med'],
        'Personna 74': ['person.*74'],
        'Personna Red': ['personn*a.*red'],
        'Personna Blue': ['personn*a.*blue'],
        'Polsilver': ['pol(i|-)*silver', 'polsiver'],
        'Rapira Platinum Lux': ['rapira'],
        'Rapira Swedish': ['rapira.*swe'],
        'Rockwell': ['rockwell'],
        'Schick Injector': ['schick'],
        'Schick Proline': ['proline'],
        'Shark Chrome': ['shark.*chr'],
        'Shark Stainless': ['shark'],
        'Shark Platinum': ['shark.*pla'],
        'Silver Star - Super Stainless': ['silver.*star.*stain'],
        'Super-Max Blue Diamond': ['super.*max.*blu.*dia'],
        'Super-Max Platinum': ['super.*max.*plat'],
        'Super-Max Super Stainless': ['super.*max.*stai'],
        'Treet Dura Sharp': ['treet.*dura.*shar'],
        'Treet Platinum': ['treet.*pla'],
        'Viking\'s Sword Stainless': ['vik.*swor.*sta'],
        'Wilkinson Sword': ['wilk.*swor', 'wilkinson'],
        'Wizamet': ['wizamet', 'wiz'],
        'Voskhod': ['vokshod', 'voskhod', 'voshk']
    })

if __name__ == '__main__':
    ban = BladeAlternateNamer()
    print(ban.get_principal_name('Gillette 7 O\'Clock Super Platinum'))