from abc import ABC, abstractmethod
import functools
import re
import unicodedata


class BaseNameExtractor(ABC):
    """
    Subclass this to extract specific entities - razors, blades, brushes etc
    """

    # patterns people use repeatedly to document the brush they used
    # but that we can't match to anything
    BASE_GARBAGE = ["^n/a$", "^unknown$", "^not sure$"]

    @property
    @abstractmethod
    def detect_regexps(self):
        raise NotImplementedError("subclass must implement detect_regexps")

    @staticmethod
    def _to_ascii(str_val):
        if str_val is None:
            return None
        else:
            return (
                unicodedata.normalize("NFKD", str_val)
                .encode("ascii", "ignore")
                .strip()
                .decode("ascii")
            )

    @staticmethod
    def post_process_name(callback):
        # decorator that can be implemented across subclasses
        # to shared fixup on entity names before they are returned
        @functools.wraps(callback)
        def wrapped(inst, *args, **kwargs):
            entity_name = callback(inst, *args, **kwargs)
            replacements = [
                ("|", ""),
                ("&#39;", "'"),
                ("&quot;", '"'),
                ("&amp;", "&"),
            ]
            if entity_name:
                for replacement in replacements:
                    entity_name = entity_name.replace(*replacement)
                return re.sub(r"[\t|]", "", entity_name)
            else:
                return entity_name

        return wrapped

    def get_name(self, comment):
        # generally this gets overwritten by subclasses since they have entity type specific fixups
        comment_text = self._to_ascii(comment["body"])
        # try to extract entity name using regexps - ie SOTD is in a common format
        for detector in self.detect_regexps:
            res = detector.search(comment_text)
            if res:
                name = res.group(1).strip()
                for pattern in self.BASE_GARBAGE:
                    if re.search(pattern, name, re.IGNORECASE):
                        return None
                return name

        # # if we cant find the the entity by looking for it in common SOTD formats,
        # # try and find any common entity name within the comment
        # principal_name = self.alternative_namer.get_principal_name(comment_text)
        # if principal_name:
        #     return principal_name

        return None
