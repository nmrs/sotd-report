from blade_parser import BladeParser
from razor_parser import RazorParser
from base_name_extractor import BaseNameExtractor
from blade_name_extractor import BladeNameExtractor
from razor_name_extractor import RazorNameExtractor


class BladeFormatExtractor(BaseNameExtractor):

    __blade_name_extractor: BladeNameExtractor = None
    __blade_parser: BladeParser = None
    __razor_name_extractor: RazorNameExtractor = None
    __razor_parser: RazorParser = None

    def __init__(
        self, blade_name_extractor, blade_parser, razor_name_extractor, razor_parser
    ):
        self.__blade_name_extractor = blade_name_extractor
        self.__blade_parser = blade_parser
        self.__razor_name_extractor = razor_name_extractor
        self.__razor_parser = razor_parser

    def detect_regexps(self):
        raise NotImplementedError()

    def get_name(self, comment):
        FIELD = "format"
        blade = self.__blade_name_extractor.get_name(comment)
        if blade is not None:
            format = self.__blade_parser._get_value(blade, FIELD)
            if format is not None:
                return format
        razor = self.__razor_name_extractor.get_name(comment)
        if razor is not None:
            format = self.__razor_parser._get_value(razor, FIELD)
            if format is not None:
                return format

        # default to DE. Possibly correct?
        return "DE"
