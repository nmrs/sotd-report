import datetime
from dateutil.relativedelta import relativedelta
import praw

from sotd_collator.sotd_post_locator import SotdPostLocator

if __name__ == "__main__":
    start_month = curr_month = datetime.date(2024, 1, 1)
    # start_month = curr_month = datetime.date(2019,11,1)
    end_month = datetime.date(2024, 1, 1)
    # end_month = date.today().replace(day=1) - relativedelta(months=1)
    print(f"building cache for {start_month} to {end_month}")

    pr = praw.Reddit("reddit")
    pl = SotdPostLocator(pr)

    # comments = []
    while curr_month <= end_month:
        threads = pl.get_threads_for_given_month(curr_month)
        # comments = pl.get_comments_for_given_month_cached(curr_month, False)
        print(f"{format(curr_month)} - {len(threads)} threads")
        curr_month += relativedelta(months=1)
