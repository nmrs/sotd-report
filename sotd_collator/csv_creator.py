
import datetime
from dateutil import relativedelta
import pickle
from collections import defaultdict
from pickle import UnpicklingError
import praw

from razor_name_extractor import RazorNameExtractor
from sotd_post_locator import SotdPostLocator
from alternate_razor_names import AlternateRazorNames

CACHE_DIR = '../misc/'
# only report razors with >= this many shaves
OUTPUT = '../misc/sotd_razor_stats.csv'



pr = praw.Reddit('standard_creds', user_agent='arach')
pl = SotdPostLocator(pr)
rn = RazorNameExtractor()
arn = AlternateRazorNames()
#

def disk_caching_lookup_of_comments(lookup_month):
    # be kind to reddit, persist results to disk so we dont hit it everytime we change the razor cleanup / processing
    cache_file = '{0}{1}{2}.cache'.format(CACHE_DIR, lookup_month.year, lookup_month.month)

    try:
        with open(cache_file, 'rb') as f_cache:
            return pickle.load(f_cache)
    except (FileNotFoundError, UnpicklingError):
        comments = []
        for thread in pl.get_threads_for_given_month(lookup_month):
            comments.extend([x.body for x in thread.comments])

        with open(cache_file, 'wb') as f_cache:
            pickle.dump(comments, f_cache)

        return comments


fout = open(OUTPUT, 'w')
fout.write('Month,Razor,Shaves,Pct of total shaves in month\n')

start_month = curr_month = datetime.date(2016,6,1)
end_month = datetime.date(2020,2,1)

while curr_month <= end_month:
    total_shaves_for_month = 0
    raw_usage = defaultdict(int)
    clustered_usage = defaultdict(int)

    print('Processing {0}'.format(curr_month))
    for comment in disk_caching_lookup_of_comments(curr_month):
        razor_name = rn.get_name(comment)
        if razor_name is not None:
            raw_usage[razor_name] += 1

    for razor_name, uses in raw_usage.items():
        if not razor_name:
            continue
        principal_name = arn.get_principal_name(razor_name)
        if principal_name:
            clustered_usage[principal_name] += uses
        else:
            # avoid nulls
            clustered_usage[razor_name] += uses
        total_shaves_for_month += uses

    for razor_name, num_shaves in sorted(clustered_usage.items(), key=lambda item: item[1], reverse=True):
        fout.write('{0},{1},{2},{3:0.2f}\n'.format(
            *[curr_month.strftime(('%Y-%m-%d')), razor_name, num_shaves, num_shaves * 100.0 / total_shaves_for_month]
        ))


    curr_month += relativedelta.relativedelta(months=1)

fout.close()