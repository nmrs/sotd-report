from functools import cached_property, lru_cache
from mimetypes import init
import re

from base_parser import BaseParser
from razor_parser import RazorParser


class StraightWidthParser(BaseParser):
    """
    Amalgamate names
    """

    def __init__(self, rp):
        self.rp = rp

    # @cached_property
    # def __mapper(self):
    #     output = {}
    #     return output

    @lru_cache(maxsize=None)
    def _get_value(self, input_string: str, field: str) -> str:
        format = self.rp._get_value(input_string, "format")
        if format != "Straight":
            return None
        width = self.rp._get_value(input_string, "width")
        if width:
            return width

        pattern = r"\d{1,2}/(8|16)"
        match = re.search(pattern, input_string, re.IGNORECASE)
        if match:
            return match.group(0)
        return None


class StraightPointParser(BaseParser):
    """
    Amalgamate names
    """

    def __init__(self, rp):
        self.rp = rp

    _patterns = {
        "Barber's Notch": ["barber"],
        "French": ["french"],
        "Round": [r"\bround\b.*(point|tip)"],
        "Spanish": ["spanish", "elite carbon"],
        "Square": ["square"],
    }

    # @cached_property
    # def __mapper(self):
    #     output = {}
    #     return output

    @lru_cache(maxsize=None)
    def _get_value(self, input_string: str, field: str) -> str:

        format = self.rp._get_value(input_string, "format")
        if format != "Straight":
            return None

        point = self.rp._get_value(input_string, "point")
        if point:
            return point

        for name, patterns in self._patterns.items():
            for pattern in patterns:
                if re.search(pattern, input_string, re.IGNORECASE):
                    return name

        return None


class StraightGrindParser(BaseParser):

    def __init__(self, rp):
        self.rp = rp

    """
    Amalgamate names
    """

    _patterns = {
        "Extra Hollow": ["extra hollow"],
        "Half Hollow": ["half hollow"],
        "Quarter Hollow": ["quarter hollow"],
        "Pretty Hollow": ["pretty hollow"],
        "Full Hollow": ["full hollow", "hollow"],
        "Near Wedge": ["near wedge"],
        "Wedge": ["wedge"],
        "Frameback": ["frame-?back"],
    }

    # @cached_property
    # def __mapper(self):
    #     output = {}
    #     return output

    @lru_cache(maxsize=None)
    def _get_value(self, input_string: str, field: str) -> str:

        format = self.rp._get_value(input_string, "format")
        if format != "Straight":
            return None

        grind = self.rp._get_value(input_string, "grind")
        if grind:
            return grind

        for name, patterns in self._patterns.items():
            for pattern in patterns:
                if re.search(pattern, input_string, re.IGNORECASE):
                    return name

        return None


if __name__ == "__main__":
    rp = StraightWidthParser()
    # print(arn.all_entity_names)
