import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import praw

from sotd_post_locator import SotdPostLocator

start_month = curr_month = datetime.date(2023,5,1)
# start_month = curr_month = datetime.date(2019,11,1)
end_month = datetime.date(2023,5,1)
# end_month = date.today().replace(day=1) - relativedelta(months=1)
print(f'building cache for {start_month} to {end_month}')

pr = praw.Reddit("reddit")
pl = SotdPostLocator(pr)

comments = []
while curr_month <= end_month:  
    comments = pl.get_comments_for_given_month_cached(curr_month, True)
    curr_month += relativedelta(months=1)
