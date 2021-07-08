import datetime
from collections import defaultdict
from pprint import pprint

import praw
import pandas as pd
from sotd_collator.sotd_post_locator import SotdPostLocator

from psaw import PushshiftAPI

PIF_FLAIRS = ['PIF - Winner', 'PIF - Closed', 'PIF - Open']
pr = praw.Reddit('standard_creds', user_agent='arach')
ps = PushshiftAPI(pr)
pl = SotdPostLocator(pr)

# use the number of comments to determine whether this is a pif or a winner announcement
# (winner announcements have fewer comments so we can use this to exclude them)
MIN_PIF_COMMENTS = 20

res = ps.search_submissions(
    subreddit='wetshaving',
    limit=40000,
)

pifs = pd.DataFrame(columns=['title', 'created', 'user'])

cur = 0


for x in res:

    if x.link_flair_text not in PIF_FLAIRS:
        continue

    try:
        author = x.author.name
    except AttributeError:
        # deleted thread
        continue

    if x.num_comments >= MIN_PIF_COMMENTS:
        pifs.loc[cur] = [x.title,  datetime.datetime.utcfromtimestamp(x.created_utc), author]
        cur += 1

# print(pifs)
print(pifs)
print(pifs.to_markdown())

grouped = pifs.groupby('user').count().reset_index()
grouped.columns = ['user', '#pifs', 'discard']

grouped = grouped[['user', '#pifs']].sort_values(by='#pifs', ascending=False)

print(grouped.to_markdown())

# print(pifs.groupby('user').count()[['user','title']].to_markdown())