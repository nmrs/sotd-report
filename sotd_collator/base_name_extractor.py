import unicodedata


class BaseNameExtractor(object):
    """
    Subclass this to extract specific entities - razors, blades, brushes etc
    """

    @property
    def alternative_namer(self):
        raise NotImplementedError('subclass must implement alternative_namer')

    @property
    def detect_regexps(self):
        raise NotImplementedError('subclass must implement detect_regexps')

    @staticmethod
    def _to_ascii(str_val):
        if str_val is None:
            return None
        else:
            return unicodedata.normalize('NFKD', str_val).encode('ascii', 'ignore').strip().decode('ascii')

    def get_name(self, comment_text):
        comment_text = self._to_ascii(comment_text)
        for detector in self.detect_regexps:
            res = detector.search(comment_text)
            if res:
                return res.group(1).strip()

        principal_name = self.alternative_namer.get_principal_name(comment_text)
        if principal_name:
            return principal_name

        return None
