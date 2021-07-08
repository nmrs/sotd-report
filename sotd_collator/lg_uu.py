import datetime

import praw
import pandas as pd
from dateutil.relativedelta import relativedelta

from sotd_collator.sotd_post_locator import SotdPostLocator

pr = praw.Reddit('standard_creds', user_agent='arach')
pl = SotdPostLocator(pr)

years = [2016, 2017, 2018, 2019, 2020, 2021]

df = pd.DataFrame(columns=['month', 'unique users'])
df_cur = 0

for year in years:
    cur_day = datetime.date(year,6,1)
    end_day = datetime.date(year,6,30)





    while cur_day <= end_day:

        uu = set()

        for comment, user_id in pl.get_comments_for_given_day_cached(cur_day, filter_pattern='games'):
            uu.add(user_id)

        df.loc[df_cur] = [cur_day.strftime('%Y-%m-%d'), len(uu)]

        df_cur += 1
        cur_day += relativedelta(days=1)


print(df.to_markdown(showindex=False))