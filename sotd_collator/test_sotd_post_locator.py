import calendar
import datetime
from unittest import TestCase
from numpy import equal
import praw
from dateutil import relativedelta
import pandas as pd

from sotd_collator.sotd_post_locator import SotdPostLocator

# from sotd_collator.sotd_post_locator import SotdPostLocator

'Wednesday SOTD Thread (6 Oct 2021)'

class TestSotdPostLocator(TestCase):

    def test_extract_date_from_title(self):
        test_cases = [
            {
                "case": 'Theme Thursday SOTD Thread - Dec. 06, 2018',
                "expected_result": datetime.date(2018, 12, 6)
            },
            {
                "case": 'Wednesday SOTD Thread (6 Oct 2021)',
                "expected_result": datetime.date(2021, 10, 6)
            },
        ]

        pr = praw.Reddit('reddit')
        pl = SotdPostLocator(pr)
        
        for case in test_cases:
            result = pl.extract_date_from_thread_title(case['case'])
            self.assertEqual(case["expected_result"], result)




#     longMessage = True

#     # CONCLUDE WE CAN GO BACK TO 2016-05-01

#     def test_get_threads_for_given_month_from_reddit(self):
#         # not really a unit test per se - see how far back we can reliably get all threads for a given month
#         spl = SotdPostLocator(praw.Reddit("reddit"))
#         first_month = datetime.date(2016, 5, 1)
#         last_month = datetime.date.today().replace(day=1) - relativedelta.relativedelta(
#             months=1
#         )
#         test_months = pd.date_range(first_month, last_month, freq="MS").to_list()
#         test_months = [datetime.date(2016, 5, 1)]
#         # sotd_thread_matcher_re = '(?:Mon(?:day)?|Tue(?:s(?:day)?)?|Wed(?:nesday)?|Thu(?:rs(?:day)?)?|Fri(?:day)?|Sat(?:urday)?|Sun(?:day)?)\sSOTD\sThread\].*$'
#         for test_month in test_months:
#             days = []
#             expected_days = calendar.monthrange(test_month.year, test_month.month)
#             for x in range(0, expected_days[1]):
#                 days.append(None)

#             print(f"testing {test_month}")
#             threads = spl.get_threads_for_given_month(test_month)
#             for thread in threads:
#                 day = datetime.date.fromtimestamp(thread.created_utc).day - 1
#                 days[day] = thread.title

#             matches = [i for i in days if i is not None]

#             expected_days = calendar.monthrange(test_month.year, test_month.month)
#             # check whether this is full set of days from that month
#             if len(matches) != expected_days[1]:
#                 for thread in threads:
#                     print(thread.title)
#             self.assertEqual(
#                 len(matches),
#                 expected_days[1],
#                 f"Testing {test_month}. Expected {expected_days[1]} but found {len(matches)}",
#             )


if __name__ == "__main__":
    tspl = TestSotdPostLocator()
    # tspl.test_get_threads_for_given_month_from_reddit()
    tspl.test_extract_date_from_title()
