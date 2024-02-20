import re
from functools import cached_property, lru_cache
from base_parser import BaseParser
from razor_parser import RazorParser
from sotd_collator.base_name_extractor import BaseNameExtractor


class KarvePlateParser(BaseParser):
    """
    From a given comment, if it's a Karve CB then extract the plate used if possible
    """

    def __init__(self, rp: RazorParser) -> None:
        self.rp = rp

    oc_re = re.compile(r"\b(OC|open.*comb)\b", re.IGNORECASE)
    plate_re = re.compile(r"[\s(\-]([A-G](?<=A)*)(?:$|\s|-plate|\))", re.IGNORECASE)

    @lru_cache(maxsize=None)
    def _get_value(self, input_string: str, field: str) -> str:
        razor_name = self.rp.get_value(input_string, "name")
        if razor_name != "Karve Christopher Bradley":
            return None

        try:
            plate = self.plate_re.search(input_string).group(1)
        except AttributeError:
            return None

        # determine OC / SB
        sb_oc = "OC" if self.oc_re.search(input_string) else "SB"

        return f"{plate} {sb_oc}"
