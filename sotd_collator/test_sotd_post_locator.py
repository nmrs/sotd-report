import datetime
import re
from unittest import TestCase
from calendar import monthrange
import praw
from dateutil import relativedelta

from sotd_post_locator import SotdPostLocator


class TestSotdPostLocator(TestCase):

    #CONCLUDE WE CAN GO BACK TO 2016-05-01


    def test_get_threads_for_given_month(self):

        # not really a unit test per se - see how far back we can reliably get all threads for a given month
        spl = SotdPostLocator(praw=praw.Reddit('standard_creds', user_agent='arach'))
        initial_month = datetime.date(2016,1,1)
        test_month = datetime.date.today().replace(day=1) - relativedelta.relativedelta(months=1)
        test_month = datetime.date(2016,3,1)
        while test_month >= initial_month:
            print('testing {0}'.format(test_month))
            threads = spl.get_threads_for_given_month(test_month)
            days_present = set()
            for thread in threads:
                match = re.search(r'\w{3} \d{2}, \d{4}', thread.title)
                if match:
                    days_present.add(datetime.datetime.strptime(match.group(0), '%b %d, %Y').date())
                else:
                    # some threads are misnamed, use the utc date instead
                    days_present.add(datetime.datetime.utcfromtimestamp(thread.created_utc).date())

            expected_days = [datetime.date(int(test_month.year), int(test_month.month), int(x)) for x in range(1, monthrange(test_month.year, test_month.month)[1] + 1)]
            # check whether this is full set of days from that month

            self.assertEqual(set(expected_days), days_present)
            test_month -= relativedelta.relativedelta(months=1)

