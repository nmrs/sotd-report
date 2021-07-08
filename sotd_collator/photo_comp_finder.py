## find entries from the photo competition for the lather games
import datetime
from pprint import pprint

import praw
import re
import csv

from sotd_collator.sotd_post_locator import SotdPostLocator

DAY_TO_PROCESS = datetime.date(2021, 6, 30)

TAG_STRING = '#photocontest'

pl = SotdPostLocator(praw.Reddit('standard_creds', user_agent='arach'))
img_re = re.compile(r'https*://[\w.]*imgur[\w.]+/[\w./]+')

res = pl.get_comments_for_given_day_cached(DAY_TO_PROCESS, filter_pattern='games', use_author_name=True)

output = list()

for comment, username in res:
    if TAG_STRING.lower() in comment.lower():
        m = img_re.search(comment)
        if m:
            output.append([DAY_TO_PROCESS.strftime('%Y-%m-%d'), username, m.group(0)])



with open('../misc/photo_entries_{0}.csv'.format(DAY_TO_PROCESS.strftime('%Y-%m-%d')), 'w') as fout:
 c = csv.writer(fout)
 for row in output:
     c.writerow(row)
