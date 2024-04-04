import re
from base_parser import BaseParser
from razor_parser import RazorParser


class GameChangerPlateParser(BaseParser):
    """
    From a given comment, if it's a Game Changer then extract the plate used if possible
    """

    def __init__(self, rp: RazorParser) -> None:
        self.rp = rp

    oc_re = re.compile(r"\b(OC|open.*comb)\b", re.IGNORECASE)
    jaws_re = re.compile(r"\b(jaws)\b", re.IGNORECASE)
    plate_re = re.compile(r"\s*(\d{3}|\d{2}|\d\.\d{2})\s*", re.IGNORECASE)

    def _get_value(self, input_string: str, field: str) -> str:
        razor_name = self.rp.get_value(input_string, "name")
        if razor_name != "RazoRock Game Changer":
            return None

            # extract plate from name

        plate = None
        try:
            plate = (
                self.plate_re.search(input_string)
                .group(1)
                .replace(".", "")
                .replace(",", "")
            )
        except AttributeError:
            return None

        if len(plate) == 2:
            plate = f".{plate}"
        elif len(plate) == 3:
            plate = f"{plate[0]}.{plate[1:3:1]}"

        gap = str(round(float(plate.removeprefix("0")), 2)).removeprefix("0")
        plate = f"{gap}-P"

        if plate in [".85-P", ".94-P"]:
            plate = ".84-P"

        # determine if OC or JAWS
        if self.jaws_re.search(input_string):
            plate_type = "JAWS"
        elif self.oc_re.search(input_string):
            plate_type = "OC"
        else:
            plate_type = ""

        res = f"{plate} {plate_type}".strip()
        # print(res)
        return res
