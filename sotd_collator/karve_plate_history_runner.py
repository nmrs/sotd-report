import datetime
import pandas as pd
import pkg_resources

import praw
from dateutil.relativedelta import relativedelta

from sotd_collator.karve_plate_extractor import KarvePlateExtractor
from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.utils import (
    add_ranking_delta,
    get_shave_data_for_month,
    get_shaving_histogram,
    get_entity_histogram,
)

pr = praw.Reddit("standard_creds", user_agent="arach")
pl = SotdPostLocator(pr)
OUT_FILE = pkg_resources.resource_filename(
    "sotd_collator", "../misc/karve_plate_history.csv"
)

# only report entities with >= this many shaves
MIN_SHAVES = 5

cur_month = start_month = datetime.date(2018, 9, 1)
end_month = datetime.date(2020, 8, 1)

all_usage = pd.DataFrame(columns=["name", "shaves", "unique users", "month"])

while cur_month <= end_month:
    print(cur_month)
    usage = get_shave_data_for_month(cur_month, pl, KarvePlateExtractor(), None)
    usage.drop("rank", inplace=True, axis=1)
    usage.drop("avg shaves per user", inplace=True, axis=1)

    # remove nulls
    usage.dropna(subset=["name"], inplace=True)

    usage.loc[:, "month"] = cur_month.strftime("%Y-%m-%d")

    all_usage = pd.concat([usage, all_usage])
    cur_month += relativedelta(months=1)


all_usage.to_csv(OUT_FILE, index=False)
