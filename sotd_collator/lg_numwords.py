import datetime

import praw
import pandas as pd
from dateutil.relativedelta import relativedelta

from sotd_collator.sotd_post_locator import SotdPostLocator

pr = praw.Reddit('standard_creds', user_agent='arach')
pl = SotdPostLocator(pr)

years = [2016, 2017, 2018, 2019, 2020, 2021]

df = pd.DataFrame(columns=['day', 'year', 'unique users'])
df_cur = 0

def _has_alpha(word):
    return [s for s in word if s.isalpha()]

def get_num_tokens(text):
    return len([x for x in text.split() if _has_alpha(x)])

for year in years:
    cur_day = datetime.date(year,6,1)
    end_day = datetime.date(year,6,30)

    while cur_day <= end_day:

        total_tokens = 0
        total_comments = 0

        for comment, user_id in pl.get_comments_for_given_day_cached(cur_day, filter_pattern='games'):
            total_tokens += get_num_tokens(comment)
            total_comments += 1

        if total_comments > 0:

            df.loc[df_cur] = [cur_day.strftime('%Y-%m-%d'), cur_day.year, 1.0 * total_tokens / total_comments]

        df_cur += 1
        cur_day += relativedelta(days=1)


print(df.to_markdown(showindex=False))