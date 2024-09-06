from collections import OrderedDict
from functools import cached_property, lru_cache
import os
from unittest.mock import Base

import yaml
from base_parser import BaseParser
import re


class BladeParser(BaseParser):
    """
    Amalgamate names
    """

    # @lru_cache(maxsize=1024)
    # def get_principal_name(self, name):
    #     stripped = self.remove_digits_in_parens(name)
    #     return super().get_principal_name(stripped)

    @cached_property
    def __blades_from_yaml(self):
        with open(f"{os.getcwd()}/sotd_collator/blades.yaml", "r") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)

    @cached_property
    def __mapper(self):
        output = {}
        for name, property_map in self.__blades_from_yaml.items():
            for pattern in property_map["patterns"]:
                format = property_map["format"] if "format" in property_map else "DE"
                output[pattern] = {"name": name, "format": format}
        return output

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
        regexes = sorted(self.__mapper.keys(), key=len, reverse=True)
        for alt_name_re in regexes:
            if re.search(alt_name_re, input_string, re.IGNORECASE):
                property_map = self.__mapper[alt_name_re]
                if field in property_map:
                    return self.__mapper[alt_name_re][field]
                # else:
                #     raise ValueError(f"Unsupported field: {field}")
        return None


if __name__ == "__main__":

    class CustomDumper(yaml.Dumper):
        def represent_data(self, data):
            if isinstance(data, str) and "\\" in data:
                return self.represent_scalar("tag:yaml.org,2002:str", data, style="'")

            return super(CustomDumper, self).represent_data(data)

    bp = BladeParser()
    # print(rp._razors_from_yaml)

    with open(f"{os.getcwd()}/sotd_collator/blades.yaml", "w") as f:
        yaml.dump(bp._raw, f, default_flow_style=False, Dumper=CustomDumper)
