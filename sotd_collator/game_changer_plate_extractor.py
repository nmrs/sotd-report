import re
from functools import cached_property
from sotd_collator.base_name_extractor import BaseNameExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer


class GameChangerPlateExtractor(BaseNameExtractor):
    """
    From a given comment, if it's a Game Changer then extract the plate used if possible
    """

    oc_re = re.compile(r"\b(OC|open.*comb)\b", re.IGNORECASE)
    jaws_re = re.compile(r"\b(jaws)\b", re.IGNORECASE)
    plate_re = re.compile(r"\s*(\d{3}|\d{2}|\d\.\d{2})\s*", re.IGNORECASE)

    @cached_property
    def alternative_namer(self):
        return RazorAlternateNamer()

    @cached_property
    def detect_regexps(self):
        razor_name_re = r"""\w\t ./\-_()#;&\'\"|<>:$~"""

        return [
            re.compile(
                r"^[*\s\-+/]*Razor\s*[:*\-\\+\s/]+\s*([{0}]+)(?:\+|,|\n|$)".format(
                    razor_name_re
                ),
                re.MULTILINE | re.IGNORECASE,
            ),  # TTS and similar
            re.compile(
                r"\*Razor\*:.*\*\*([{0}]+)\*\*".format(razor_name_re),
                re.MULTILINE | re.IGNORECASE,
            ),  # sgrddy
            re.compile(
                r"^\*\*Safety Razor\*\*\s*-\s*([{0}]+)[+,\n]".format(razor_name_re),
                re.MULTILINE | re.IGNORECASE,
            ),  # **Safety Razor** - RazoRock - Gamechanger 0.84P   variant
        ]

    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        comment_text = self._to_ascii(comment["body"])
        extracted_name = None

        for detector in self.detect_regexps:
            res = detector.search(comment_text)
            # catch case where some jerk writes ❧ Razor and Blade Notes or similar
            # at some point this can be genericised in to a block words / phrases list to catch razorock too
            if res and "and blade note" in res.group(1).lower():
                continue

            # catch case where we match against razorock
            if res and not (len(res.group(1)) >= 3 and res.group(1)[0:3] == "ock"):
                extracted_name = res.group(1)

        if not extracted_name:
            return None

        principal_name = self.alternative_namer.get_principal_name(extracted_name)
        if not principal_name or not principal_name.startswith("Razorock Game Changer"):
            return None

        # extract plate from name
        try:
            plate = (
                self.plate_re.search(extracted_name)
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

        plate = "{0}-P".format(
            str(round(float(plate.removeprefix("0")), 2)).removeprefix("0")
        )

        # determine if OC or JAWS
        if self.jaws_re.search(extracted_name):
            plate_type = "JAWS"
        elif self.oc_re.search(extracted_name):
            plate_type = "OC"
        else:
            plate_type = ""

        res = f"{plate} {plate_type}".strip()
        # print(res)
        return res
