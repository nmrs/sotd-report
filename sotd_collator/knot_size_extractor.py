import re
from functools import cached_property
from sotd_collator.base_name_extractor import BaseNameExtractor


class KnotSizeExtractor(BaseNameExtractor):
    """
    From a given comment, extract the brush size name
    """

    @cached_property
    def detect_regexps(self):
        brush_size_re = r"""\d{2}\s*mm"""

        return [
            re.compile(r'^[*\s\-+/]*brush\s*[:*\-\\+\s/]+[^:]*({0})'.format(brush_size_re), re.MULTILINE | re.IGNORECASE),  # TTS and similar
            re.compile(r'\*brush\*:.*\*\*[^:]({0})'.format(brush_size_re), re.MULTILINE | re.IGNORECASE),  # sgrddy
            # if we cant find it in a specific brush line, search the entire post
           re.compile(r'({0})'.format(brush_size_re), re.MULTILINE | re.IGNORECASE),

       ]

    @BaseNameExtractor.post_process_name
    def get_name(self, comment_text):

        comment_text = self._to_ascii(comment_text)
        for detector in self.detect_regexps:
            res = detector.search(comment_text)
            if res:
                raw_size = res.group(1)
                num_mm = int(re.search('\d+', raw_size).group(0))
                if num_mm < 18 or num_mm > 32:
                    # probably a mistake, these are outside the usual brush sizes
                    continue
                return re.sub('\s+', '', raw_size.strip().lower())

        return None
