from functools import cached_property, lru_cache
import os
import re
import yaml

from base_parser import BaseParser


class SoapParser(BaseParser):
    """
    Amalgamate names
    """

    @cached_property
    def __soaps_from_yaml(self):
        with open(f"{os.getcwd()}/sotd_collator/soaps.yaml", "r") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)

    @cached_property
    def __mapper(self):
        output = {}

        data = None

        # for brand, brand_map in self._raw.items():
        for brand, brand_map in self.__soaps_from_yaml.items():
            scents = brand_map["scents"] if "scents" in brand_map else {}
            for scent, property_map in scents.items():
                for pattern in property_map["patterns"]:
                    format = (
                        property_map["format"] if "format" in property_map else "Soap"
                    )
                    name = f"{brand} - {scent}".strip()
                    # if format != "Soap":
                    #     name = f"{name} ({format})"

                    output[pattern] = {
                        "brand": brand,
                        "scent": scent,
                        "name": name,
                        "format": format,
                    }
        return output

    @cached_property
    def __brand_map(self):
        output = {}
        # for brand, property_map in self._raw.items():
        for brand, property_map in self.__soaps_from_yaml.items():
            for pattern in property_map["patterns"]:
                output[pattern] = {
                    "brand": brand,
                    "default format": (
                        property_map["default format"]
                        if "default format" in property_map
                        else "Soap"
                    ),
                }
        return output

    @lru_cache(maxsize=None)
    def _get_value(self, input_string: str, field: str) -> str:

        input_string = input_string.replace("*", "").replace("(sample)", "").strip()
        regexes = sorted(self.__mapper.keys(), key=len, reverse=True)
        for alt_name_re in regexes:
            if re.search(alt_name_re, input_string, re.IGNORECASE):
                property_map = self.__mapper[alt_name_re]
                if field in property_map:
                    return property_map[field]

        # we didn't find an exact scent, try to match at least brand by regex
        regexes = sorted(self.__brand_map.keys(), key=len, reverse=True)
        for alt_name_re in regexes:
            match = re.search(alt_name_re, input_string, re.IGNORECASE)
            if match:
                property_map = self.__brand_map[alt_name_re]
                brand = property_map["brand"]
                map = self.split_name(input_string)
                scent = map["scent"] if map is not None else None
                if scent is None:
                    # strip brand out of input string and scent is what is left at the end
                    scent = (
                        input_string.replace(match.group(0), "")
                        .strip()
                        .removeprefix("-")
                        .removesuffix(".")
                        .strip()
                    )
                    scent = " ".join(scent.split())

                name = f"{brand} - {scent}"
                format = map["format"] if map is not None and "format" in map else None
                if format is None:
                    if re.search(r"\bcream\b", name, re.IGNORECASE):
                        format = "Cream"
                    elif re.search(r"\bfoam", name, re.IGNORECASE):
                        format = "Foam"

                if format is None:
                    format = (
                        property_map["default format"]
                        if "default format" in property_map
                        else "Soap"
                    )
                # if format != "Soap":
                #     name = f"{name} ({format})"

                map = {
                    "brand": brand,
                    "scent": scent,
                    "name": name,
                    "format": format,
                }

                return map[field]

        # return None
        map = self.split_name(input_string)
        return map[field] if map is not None else None

    def split_name(self, input_string: str):

        match = re.search(r"\(\d{1,3}\)", input_string)
        if match:
            input_string = input_string.replace(match.group(0), "")

        input_string = input_string.replace("—", "-").replace("–", "-")
        parts = input_string.split(" - ")
        while "   " in input_string:
            input_string = input_string.replace("   ", "  ")

        if len(parts) < 2:
            parts = input_string.split("  ")

        result = {}
        if len(parts) > 1:

            scent = parts[1].strip().removesuffix(".").strip()
            suffixes = ["soap", "soap", "shaving soap", "-"]
            for suffix in suffixes:
                match = re.search(suffix, scent, re.IGNORECASE)
                if match:
                    scent = scent.replace(match.group(0), "")

            result["brand"] = parts[0].strip()
            result["scent"] = scent
            result["name"] = f"{parts[0].strip()} - {scent}"
            # result["format"] = "Soap"

            if len(parts) > 2:
                if re.search("soap", parts[2], re.IGNORECASE):
                    result["format"] = "Soap"
                elif re.search("cream", parts[2], re.IGNORECASE):
                    result["format"] = "Cream"
                elif re.search("foam", parts[2], re.IGNORECASE):
                    result["format"] = "Foam"
                else:
                    result["format"] = "Soap"
            else:
                if re.search("soap", parts[1], re.IGNORECASE):
                    result["format"] = "Soap"
                elif re.search("cream", parts[1], re.IGNORECASE):
                    result["format"] = "Cream"
                elif re.search("foam", parts[1], re.IGNORECASE):
                    result["format"] = "Foam"
                else:
                    result["format"] = "Soap"

            return result

        return None


if __name__ == "__main__":

    class CustomDumper(yaml.Dumper):
        def represent_data(self, data):
            if isinstance(data, str) and ("\\" in data or "?" in data):
                return self.represent_scalar("tag:yaml.org,2002:str", data, style="'")

            return super(CustomDumper, self).represent_data(data)

    rp = SoapParser()
    raw = None
    with open(f"{os.getcwd()}/sotd_collator/soaps.yaml", "r") as f:
        raw = yaml.load(f, Loader=yaml.SafeLoader)

    with open(f"{os.getcwd()}/sotd_collator/soaps.yaml", "w") as f:
        yaml.dump(raw, f, default_flow_style=False, Dumper=CustomDumper)

    # print(arn.all_entity_names)
