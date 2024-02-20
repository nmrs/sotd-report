from functools import lru_cache
from blade_parser import BladeParser
from razor_parser import RazorParser


class RazorPlusBladeParser(object):
    """
    Amalgamate names
    """

    def __init__(self, razor_parser: RazorParser, blade_parser: BladeParser):
        self.__rp = razor_parser
        self.__bp = blade_parser

    @lru_cache(maxsize=None)
    def get_value(self, input_string: str, field: str = "name") -> str:
        if field != "name":
            raise ValueError('"name" is the only supported field value')

        razor_name, blade_name = input_string.split("\001", maxsplit=2)
        pr_name = self.__rp._get_value(razor_name, field)
        if pr_name:
            razor_name = pr_name
        pb_name = self.__bp._get_value(blade_name, field)
        if pb_name:
            blade_name = pb_name

        return f"{razor_name} + {blade_name}"
