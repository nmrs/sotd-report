from abc import ABC, abstractmethod
from functools import cached_property, wraps
import re
import unicodedata

import cache_provider


class BaseNameExtractor(ABC):
    """
    Subclass this to extract specific entities - razors, blades, brushes etc
    """

    # patterns people use repeatedly to document the brush they used
    # but that we can't match to anything
    __BASE_GARBAGE = ["^n/a$", "^unknown$", "^unknown unknown$" "^not sure$"]

    @property
    @abstractmethod
    def detect_regexps(self):
        raise NotImplementedError("subclass must implement detect_regexps")

    __name_chars = r"\w\t ./\-_()#;&\'\"|<>:$~\[\]"
    __imgur_name_chars = r"\w\t ./\-_()#;&\'\"|<>:$~"

    def tts_detector(self, token):
        return re.compile(
            # rf"^[*\s\-+/]*{token}\s*[:*\-\\+\s/]+\s*([{self.__name_chars}]+)(?:\+|,|\n|$)",
            # rf"^[*\s\-+/]*{token}\s*[:*\-\\+\s/]+\s*(.+)$",
            rf"^[*\s\-+/\\]*{token}\s*[:*\-\\+ \t/]*(.*)$",
            re.MULTILINE | re.IGNORECASE,
        )

    def imgur_detector(self, token):
        return re.compile(
            # rf"^[*\s\-+/]*{token}\s*[:*\-\\+\s/]+\s*\[*([{self.__imgur_name_chars}]+)(?:.*[(\[\{{](\d*)[)\]\}}]|.*)$",
            rf"^[*\s\-+/]*{token}\s*[:*\-\\+\s/]+\s*([^\[\n$]*)\[([^\]]*)\]\((?:[^\)]*)\)(.*)$",
            re.MULTILINE | re.IGNORECASE,
        )  # TTS style with link to eg imgur

    # def sgrddy_detector(self, token):
    #     return re.compile(
    #         rf"\*{token}[\*:\s]+([{self.__name_chars}]+)\*\*",
    #         re.MULTILINE | re.IGNORECASE,
    #     )

    # @abstractmethod
    def _garbage(self):
        return []

    def __garbage(self):
        return self.__BASE_GARBAGE + self._garbage()

    @staticmethod
    def _to_ascii(str_val):
        if str_val is None:
            return None
        else:
            return (
                unicodedata.normalize("NFKD", str_val).replace("•", "*")
                # .encode("ascii", "ignore")
                # .strip()
                # .decode("ascii")
            )

    @staticmethod
    def post_process_name(callback):
        # decorator that can be implemented across subclasses
        # to shared fixup on entity names before they are returned
        @wraps(callback)
        def wrapped(inst, *args, **kwargs):
            entity_name = callback(inst, *args, **kwargs)
            replacements = [
                ("|", ""),
                (r"\t", ""),
                ("&#39;", "'"),
                ("&quot;", '"'),
                ("&amp;", "&"),
            ]
            if entity_name:
                for replacement in replacements:
                    entity_name = entity_name.replace(*replacement)

                for pattern in inst.__garbage():
                    if re.search(pattern, entity_name, re.IGNORECASE):
                        return None

                entity_name = entity_name.strip()
                if len(entity_name) > 0:
                    return entity_name

            return None

            #     # return re.sub(r"[\t|]", "", entity_name)
            # else:
            #     return entity_name

        return wrapped

    @post_process_name
    def get_name(self, comment):
        # generally this gets overwritten by subclasses since they have entity type specific fixups
        comment_text = self._to_ascii(comment["body"])
        # try to extract entity name using regexps - ie SOTD is in a common format
        lines = comment_text.split("\n")
        for line in lines:
            for detector in self.detect_regexps:
                res = detector.search(line)
                if res:
                    name = ""
                    for group in res.groups():
                        if group:
                            name += group
                    # name = res.group(1)
                    # # for pattern in self.BASE_GARBAGE:
                    # #     if re.search(pattern, name, re.IGNORECASE):
                    # #         return None
                    name = self.remove_hashtags(name)
                    return name.strip()

        # # if we cant find the the entity by looking for it in common SOTD formats,
        # # try and find any common entity name within the comment
        # principal_name = self.alternative_namer.get_principal_name(comment_text)
        # if principal_name:
        #     return principal_name

        return None

    def remove_hashtags(self, text):
        # Define the regex pattern for hashtags
        pattern = r"#\w+"
        # Use re.sub() to replace hashtags with an empty string
        cleaned_text = re.sub(pattern, "", text)
        return cleaned_text.strip()
