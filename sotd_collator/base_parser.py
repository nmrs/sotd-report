from abc import ABC, abstractmethod
import re
from functools import lru_cache, cached_property
from typing import Dict


class BaseParser(ABC):
    """
    Amalgamate names
    """

    # @cached_property
    # def all_entity_names(self):
    #     unique = set()
    #     for stub, variants in self._raw.items():
    #         unique.add(stub)
    #         unique.update(variants)

    #     return list(unique)

    # @cached_property
    # def _mapper(self) -> Dict[str, str]:
    #     return self._build_mapper()

    # @abstractmethod
    # def _build_mapper(self) -> Dict[str, str]:
    #     return {}

    def remove_digits_in_parens(self, input_string):
        pattern = r"\([0-9]+\)|\[[0-9]+\]|\{[0-9]+\}"
        result = re.sub(pattern, "", input_string)
        return result

    @abstractmethod
    def _get_value(self, input_string: str, field: str) -> str:
        return None

    def get_value(self, input_string: str, field: str) -> str:
        if field == "original":
            return input_string
        else:
            return self._get_value(input_string, field)
