import re
from collections import OrderedDict
from functools import lru_cache, cached_property


class BaseAlternateNamer(object):
    """
    Amalgamate names
    """

    @cached_property
    def all_entity_names(self):
        unique = set()
        for stub, variants in self._raw.items():
            unique.add(stub)
            unique.update(variants)

        return list(unique)

    @cached_property
    def _mapper(self):
        output = {}
        for main_name, alternate_names in self._raw.items():
            for alternate_name in alternate_names:
                output[alternate_name] = main_name
        return output

    @lru_cache(maxsize=1024)
    def get_principal_name(self, name):
        for alt_name_re in sorted(self._mapper.keys(), key=len, reverse=True):
            if re.search(alt_name_re, name, re.IGNORECASE):
                return self._mapper[alt_name_re]
        return None

    _raw = OrderedDict({})

