import re
from functools import lru_cache, cached_property

from base_parser import BaseParser
from brush_parsing_stategies import (
    DeclarationGroomingParsingStrategy,
    KnownBrushStrategy,
    OmegaSemogueBrushParsingStrategy,
    ZenithBrushParsingStrategy,
    OtherBrushStrategy,
)


class BrushParser(BaseParser):
    """
    Amalgamate names
    """

    def __init__(self) -> None:
        self.__parser_strategies = (
            DeclarationGroomingParsingStrategy(),
            KnownBrushStrategy(),
            OmegaSemogueBrushParsingStrategy(),
            ZenithBrushParsingStrategy(),
            OtherBrushStrategy(),
        )

    @lru_cache(maxsize=None)
    def _get_value(self, input_string: str, field: str) -> str:
        for stategy in self.__parser_strategies:
            result = stategy.get_property_map(input_string)
            if result:
                if field in result:
                    return result[field]
                else:
                    return None
        return None


if __name__ == "__main__":
    pass
    # print(BrushAlternateNamer().get_principal_name(name="Zenith foo h24"))
