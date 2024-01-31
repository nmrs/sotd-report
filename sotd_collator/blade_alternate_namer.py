from collections import OrderedDict
from functools import lru_cache
from sotd_collator.base_alternate_namer import BaseAlternateNamer
import re


class BladeAlternateNamer(BaseAlternateNamer):
    """
    Amalgamate names
    """

    _raw = OrderedDict(
        {
            "7 O'Clock - Permasharp": ["clock.*perm"],
            "7 O'Clock - Sharpedge (Yellow)": ["clock.*sharpe", "clock.*yellow"],
            "7 O'Clock - Super Platinum (Black)": ["clock.*pla", "clock.*black"],
            "7 O'Clock - Super Stainless (Green)": [
                "clock.*sta",
                "clock.*green",
                "clock",
                "gil.*et.*super.*stain",
            ],
            "Aeterna": ["aeter"],
            "Astra Superior Platinum (Green)": [
                "astra.*plat",
                "astra.*green",
                "astra.*sp",
                "astra",
            ],
            "Astra Superior Stainless (Blue)": [
                "astra.*sta",
                "astra.*blue",
                "astra.*ss",
            ],
            "Bic Astor Stainless": ["bic.*(ast|stai)"],
            "Bic Chrome": ["bic.*(chr|pla)", "bic"],
            "Big Ben": ["big ben"],
            "Bolzano": ["b(o|a)lzano"],
            "Crystal": ["crystal"],
            "Dorco BB-20 (AC)": ["dorco.*bb*"],
            "Dorco ST-300": ["dorco.*st.*300", "dorco"],
            "Dorco ST-301": ["dorco.*st.*301"],
            "Dorco Titan": ["dorco.*titan"],
            "Derby Extra": ["derb.*extra", "derby"],
            "Derby Extra Blue": ["derb.*blue"],
            "Derby Premium": ["derb.*prem"],
            "Eddison Stainless": ["eddison"],
            "Euromax": ["euromax"],
            "Feather (DE)": [
                "feather",
                "feather.*hi.*st",
                "feather.*hs",
                "feather \s*blade",
                "feather.*de",
            ],
            "Feather FHS-1": ["fhs-1"],
            "Feather Pro (AC)": ["feather.*pro"],
            "Feather Pro Light (AC)": ["feather.*light"],
            "Feather Pro Super (AC)": ["feather.*super", "pro\s*super"],
            "Feather ProGuard (AC)": ["feather.*guard"],
            "Feather Soft Guard (AC)": ["feather.*soft"],
            "GEM Blue Star": ["gem.*blue.*star"],
            "Gillette Minora": ["minora"],
            "Gillette Nacet": ["nan*cet"],
            "Gillette Platinum": ["gil.*pla"],
            "Gillette Rubie": ["rubie"],
            "Gillette Silver Blue": [
                "gsb",
                "Gill.*sil.*blue",
                "silver.*blue",
                "gill.*sb",
                "gill.*blu.*sil",
            ],
            "Gillette Spoiler": ["gil.*et.*spoil"],
            "Gillette Wilkinson Sword": ["gil.*et.*wilk.*swor"],
            "Gillette Winner": ["gil.*winn"],
            "Kai (DE)": ["^kai$", "kai.*sta", "kai.*ss"],
            "Kai Captain Blade (AC)": ["kai.*blade", "kai captain\s*$"],
            "Kai Captain Sharpblade (AC)": ["kai.*sharp"],
            "Kai Captain Titan Mild (AC)": ["kai.*titan", "kai.*cap.*pink"],
            "Kai Captain Titan Mild Protouch (AC)": ["kai.*protouch"],
            "King C Gillette": ["king.*c.*gil.*et", "gil.*et.*king.*c"],
            "Ladas": ["lada"],
            "Lord Classic": ["lord.*cla"],
            "Lord Cool": ["lord.*cool"],
            "Lord Super Stainless": ["lord.*sup"],
            "Kismet Hair Shaper": ["kismet"],
            "Merkur Super Platinum": ["merkur"],
            "Muhle": ["muhle"],
            "Permasharp": ["perma\s*-*sharp"],
            "Personna Hair Shaper": ["personn.*hair.*shap"],
            "Personna Platinum": ["personn.*plat"],
            "Personna GEM PTFE": [
                "(person|gem).*(ptfe|pfte)",
                "gem by personna",
                "(ptfe|pfte).*(person|gem)",
                "(person|ptfe).*gem",
                "ptfe",
                "gem",  # matching just GEM to this blade per guidance here: https://www.reddit.com/r/Wetshaving/comments/19a43q7/comment/kil95r8/
            ],
            "Personna GEM Stainless": ["(personna)*gem.*stainless", "gem.*ss"],
            "Personna Injector": [
                "(person|personna).*(inject|injector)"
            ],  # unecessarily long to ensure priority of checking
            "Personna Med Prep": ["person.*med"],
            "Personna 74": ["p(?:ersonn*a)?\s*74", "pseventy-four", "p74"],
            "Personna Red": ["personn*a.*red"],
            "Personna Stainless": ["personn*a.*stainless", "personn*a.*super"],
            "Personna Blue": ["personn*a.*blue", "personn*a.*c.*c", "personn*a"],
            "Polsilver": ["pol(i|-)*silver", "polsiver"],
            "Rapira Platinum Lux": ["rapira"],
            "Rapira Swedish": ["rapira.*swe"],
            "RK Stainless": ["rk"],
            "Rockwell": ["rockwell"],
            "Schick Stainless (DE)": ["schick.*s(?:tainles)*s"],
            "Schick Injector": ["schick"],
            "Schick Proline (AC)": ["proline"],
            "Shark Chrome": ["shark.*chr"],
            "Shark Stainless": ["shark"],
            "Shark Platinum": ["shark.*pla"],
            "Silver Star - Super Stainless": ["silver.*star.*stain"],
            "Super-Max Blue Diamond": ["super.*max.*(?:blu)*.*dia"],
            "Super-Max Platinum": ["super.*max.*plat"],
            "Super-Max Super Stainless": ["super.*max.*stai"],
            "Tiger Platinum": ["tiger"],
            "Treet Dura Sharp": ["treet.*dura.*shar"],
            "Treet Platinum": ["treet.*pla"],
            "Viking's Sword Stainless": ["vik.*swor.*sta"],
            "Wilkinson Sword": ["wilk.*swor", "wilkinson"],
            "Wizamet": ["wizamet", "wiz"],
            "Voskhod": ["vokshod", "voskhod", "voshk"],
        }
    )

    @lru_cache(maxsize=1024)
    def get_principal_name(self, name):
        stripped = self.remove_digits_in_parens(name)
        return super().get_principal_name(stripped)

    def remove_digits_in_parens(self, input_string):
        pattern = r"\([0-9]+\)|\[[0-9]+\]|\{[0-9]+\}"
        result = re.sub(pattern, "", input_string)
        return result


if __name__ == "__main__":
    # ban = BladeAlternateNamer()
    # print(ban.get_principal_name('Gillette 7 O\'Clock Super Platinum'))

    print(re.search("feather.*(?:de)?", "Feather (de)", re.IGNORECASE))
