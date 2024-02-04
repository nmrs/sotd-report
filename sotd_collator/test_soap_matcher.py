from unittest import TestCase

from sotd_collator.soap_matcher import SoapMatcher


class TestSoapMatcher(TestCase):
    
    test_cases = [
        {
            "case": "Barrister & Mann - Soft Heart Series: Sandalwood",
            "expected_soap": "Barrister & Mann",
            "expected_scent": "Sandalwood",
        },
        {
            "case": "B&M - Soft Heart Series: Sandalwood",
            "expected_soap": "Barrister & Mann",
            "expected_scent": "Sandalwood",
        },
        {
            "case": "B&M - Soft Heart Series: Unknown Soap",
            "expected_soap": "Barrister & Mann",
            "expected_scent": None,
            "expected_fallback": "Soft Heart Series: Unknown Soap"
        }   
     ]

    def test_soap_cases(self):
        an = SoapMatcher()
        for case in self.test_cases:
            soap = an.get_brand(case["case"])
            self.assertEqual(case["expected_soap"], soap)

    def test_scent_cases(self):
        an = SoapMatcher()
        for case in self.test_cases:
            scent = an.get_scent(case["expected_soap"], case["case"])
            self.assertEqual(case["expected_scent"], scent)

    def test_fallback_cases(self):
        an = SoapMatcher()
        for case in self.test_cases:
            if "expected_fallback" in case:
                fallback = an.get_scent_fallback(case["case"])
                self.assertEqual(case["expected_fallback"], fallback)

if __name__ == "__main__":
    tester = TestSoapMatcher()
    tester.test_soap_cases()
    tester.test_scent_cases()
    tester.test_fallback_cases()
