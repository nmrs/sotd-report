from functools import lru_cache
import re
from tarfile import LinkOutsideDestinationError
from blade_parser import BladeParser
from razor_parser import RazorParser
from base_name_extractor import BaseNameExtractor
from blade_name_extractor import BladeNameExtractor
from razor_name_extractor import RazorNameExtractor


class RazorFormatExtractor(BaseNameExtractor):

    __blade_name_extractor: BladeNameExtractor = None
    __blade_parser: BladeParser = None
    __razor_name_extractor: RazorNameExtractor = None
    __razor_parser: RazorParser = None

    FIELD = "format"
    DE = "DE"
    HALF_DE = "Half DE"
    SHAVETTE = "Shavette"

    def __init__(
        self, blade_name_extractor, blade_parser, razor_name_extractor, razor_parser
    ):
        self.__blade_name_extractor = blade_name_extractor
        self.__blade_parser = blade_parser
        self.__razor_name_extractor = razor_name_extractor
        self.__razor_parser = razor_parser

    def detect_regexps(self):
        raise NotImplementedError()

    # @lru_cache
    def get_name(self, comment):
        blade_format = self.get_format(
            comment, self.__blade_name_extractor, self.__blade_parser
        )
        razor_format = self.get_format(
            comment, self.__razor_name_extractor, self.__razor_parser
        )

        if razor_format is not None and re.match(
            r"shavette (.*)", razor_format, re.IGNORECASE
        ):
            return razor_format

        if razor_format == self.SHAVETTE:
            if blade_format is None:
                blade_format = "Unspecified"
            # assume random DE shavettes use half DE
            elif blade_format == self.DE:
                blade_format = "Half DE"
            return f"{self.SHAVETTE} ({blade_format})"

        if blade_format == self.DE:
            # starts with so we match "Half DE" and "Half DE (multi-blade)""
            if razor_format is not None and razor_format.startswith(self.HALF_DE):
                return razor_format
            else:
                return self.DE
        elif blade_format is not None:
            return blade_format
        elif razor_format is not None:
            return razor_format

        # default to DE. Possibly correct?
        return self.DE

    def get_format(self, comment, name_extractor, parser):
        name = name_extractor.get_name(comment)
        if name is not None:
            format = parser._get_value(name, self.FIELD)
            if format is not None:
                return format
