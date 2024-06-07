import re
from functools import cached_property, lru_cache
from base_parser import BaseParser
from razor_parser import RazorParser
from sotd_collator.base_name_extractor import BaseNameExtractor


class BlackbirdPlateParser(BaseParser):
    """
    From a given comment, if it's a Blackbird then extract the plate used if possible
    """

    def __init__(self, rp: RazorParser) -> None:
        self.rp = rp

    oc_re = re.compile(r"\b(OC|open.*comb)\b", re.IGNORECASE)
    lite_re = re.compile(r"\blite\b", re.IGNORECASE)

    @lru_cache(maxsize=None)
    def _get_value(self, input_string: str, field: str) -> str:
        razor_name = self.rp.get_value(input_string, "name")
        if razor_name != "Blackland Blackbird":
            return None

        plate = "Standard"
        if self.oc_re.search(input_string) != None:
            plate = "OC"
        elif self.lite_re.search(input_string) != None:
            plate = "Lite"

        return plate
