from unittest import TestCase

from sotd_collator.soap_parser import SoapParser


class TestSoapParser(TestCase):

    test_cases = [
        {
            "case": "Barrister & Mann - Soft Heart Series: Sandalwood",
            "expected_brand": "Barrister and Mann",
            "expected_scent": "Sandalwood",
        },
        {
            "case": "B&M - Soft Heart Series: Sandalwood",
            "expected_brand": "Barrister and Mann",
            "expected_scent": "Sandalwood",
        },
        {
            "case": "B&M - Soft Heart Series: Unknown Soap",
            "expected_brand": "Barrister and Mann",
            "expected_scent": "Soft Heart Series: Unknown",
            "expected_fallback": "Soft Heart Series: Unknown",
        },
    ]

    def test_soap_cases(self):
        an = SoapParser()
        for case in self.test_cases:
            soap = an.get_value(case["case"], "brand")
            self.assertEqual(case["expected_brand"], soap)

    def test_scent_cases(self):
        an = SoapParser()
        for case in self.test_cases:
            scent = an.get_value(case["case"], "scent")
            self.assertEqual(case["expected_scent"], scent)

    def test_fallback_cases(self):
        an = SoapParser()
        for case in self.test_cases:
            if "expected_fallback" in case:
                fallback = an.get_scent_fallback(case["case"])
                self.assertEqual(case["expected_fallback"], fallback)


if __name__ == "__main__":
    tester = TestSoapParser()
    tester.test_soap_cases()
    tester.test_scent_cases()
    # tester.test_fallback_cases()
