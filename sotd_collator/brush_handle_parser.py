from collections import OrderedDict
from functools import cached_property, lru_cache
import os
from unittest.mock import Base

import yaml
from base_parser import BaseParser
import re


class BrushHandleParser(BaseParser):
    """
    Amalgamate names
    """

    _raw = {}

    # @cached_property
    def _from_yaml(self, filename):
        with open(f"{os.getcwd()}/sotd_collator/brush_yaml/{filename}.yaml", "r") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)

    @cached_property
    def __mappers(self):
        result = []
        # for filename in ["brush_handles", "other_handles"]:
        for filename in ["brush_handles"]:
            output = {}
            for name, property_map in self._from_yaml(filename).items():
                for pattern in property_map["patterns"]:
                    output[pattern] = {
                        "name": name,
                    }
            result.append(output)
        return result

    # def extract_uses(input_string):
    #     match = re.search(r"[[(](\d{1,4})[)\]]", input_string)
    #     if match:
    #         return int(match.group(1))

    #     return None

    @lru_cache(maxsize=None)
    def _get_value(self, input_string: str, field: str) -> str:
        return self.__get_value(input_string, field)
        # input_string = self.remove_digits_in_parens(input_string)
        # return self.__get_value(input_string, field)

    @lru_cache(maxsize=None)
    def __get_value(self, input_string, field):
        for mapper in self.__mappers:
            regexes = sorted(mapper.keys(), key=len, reverse=True)
            for alt_name_re in regexes:
                if re.search(alt_name_re, input_string, re.IGNORECASE):
                    property_map = mapper[alt_name_re]
                    if field in property_map:
                        return mapper[alt_name_re][field]
                    # else:
                    #     raise ValueError(f"Unsupported field: {field}")
        return None


if __name__ == "__main__":
    # ban = BladeAlternateNamer()
    # print(ban.get_principal_name('Gillette 7 O\'Clock Super Platinum'))

    print(re.search("feather.*(?:de)?", "Feather (de)", re.IGNORECASE))
    # # print(rp._razors_from_yaml)

    class CustomDumper(yaml.Dumper):
        def represent_data(self, data):
            # if isinstance(data, str) and "\\" in data:
            #     return self.represent_scalar("tag:yaml.org,2002:str", data, style="'")

            return super(CustomDumper, self).represent_data(data)

    parser = BrushHandleParser()

    with open(f"{os.getcwd()}/sotd_collator/brush_handles.yaml", "w") as f:
        yaml.dump(parser._raw, f, default_flow_style=False, Dumper=CustomDumper)
