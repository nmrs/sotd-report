import datetime

import praw
import pandas as pd
from dateutil.relativedelta import relativedelta

from sotd_collator.sotd_post_locator import SotdPostLocator

pr = praw.Reddit('standard_creds', user_agent='arach')
pl = SotdPostLocator(pr)

curr_month = datetime.date(2020,1,1)
end_month = datetime.date(2021,4,1)

df = pd.DataFrame(columns=['month', 'unique users'])
df_cur = 0

while curr_month <= end_month:

    uu = set()

    for comment, user_id in pl.get_comments_for_given_month_cached(curr_month):
        uu.add(user_id)

    df.loc[df_cur] = [curr_month.strftime('%b %Y'), len(uu)]

    df_cur += 1
    curr_month += relativedelta(months=1)


print(df.to_markdown(showindex=False))