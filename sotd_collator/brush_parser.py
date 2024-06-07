import re
from functools import lru_cache, cached_property

from base_parser import BaseParser
from brush_parsing_stategies import (
    ChiselAndHoundParsingStrategy,
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
            ChiselAndHoundParsingStrategy(),
            KnownBrushStrategy(),
            OmegaSemogueBrushParsingStrategy(),
            ZenithBrushParsingStrategy(),
            OtherBrushStrategy(),
        )

    @lru_cache(maxsize=None)
    def _get_value(self, input_string: str, field: str) -> str:
        s = None
        for strategy in self.__parser_strategies:
            result = strategy.get_property_map(input_string)
            s = strategy
            if result:
                if field in result:
                    if result[field] is not None:
                        return result[field]

        if field == "fiber":
            return s.get_fiber(input_string)
        elif field == "knot size":
            return s.get_knot_size(input_string)
        elif field == "knot maker":
            return self._get_value(input_string, "brand")

        return None


if __name__ == "__main__":
    pass
    # print(BrushAlternateNamer().get_principal_name(name="Zenith foo h24"))
