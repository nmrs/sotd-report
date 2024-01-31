from collections import OrderedDict
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.blade_alternate_namer import BladeAlternateNamer


class RazorPlusBladeAlternateNamer(object):
    """
    Amalgamate names
    """

    def __init__(self):
        self.ran = RazorAlternateNamer()
        self.ban = BladeAlternateNamer()

    def get_principal_name(self, name):
        razor_name, blade_name = name.split("\001", maxsplit=2)
        pr_name = self.ran.get_principal_name(razor_name)
        if pr_name:
            razor_name = pr_name
        pb_name = self.ban.get_principal_name(blade_name)
        if pb_name:
            blade_name = pb_name

        return "{razor} + {blade}".format(
            razor=razor_name,
            blade=blade_name,
        )
