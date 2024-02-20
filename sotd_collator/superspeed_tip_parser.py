import re
from functools import cached_property
from base_parser import BaseParser
from razor_parser import RazorParser
from sotd_collator.razor_name_extractor import RazorNameExtractor
from sotd_collator.base_name_extractor import BaseNameExtractor


class SuperSpeedTipParser(BaseParser):
    """
    From a given comment, extract the razor name
    """

    def __init__(self, rp: RazorParser) -> None:
        self.rp = rp

    def _get_value(self, input_string: str, field: str) -> str:
        razor_name = self.rp.get_value(input_string, "name")
        if razor_name != "Gillette Super Speed":
            return None

        tips = {
            "Red": ["red"],
            "Blue": ["blue"],
            "Black": ["black"],
            "Flare": ["flare", "flair"],
        }

        for k, v in tips.items():
            for pattern in v:
                if re.search(pattern, input_string, re.IGNORECASE):
                    return f"{k} Tip"

        return "Unspecified"
