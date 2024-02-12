import csv
import os
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta

import praw

from sotd_collator.base_name_extractor import BaseNameExtractor
from sotd_collator.brush_alternate_namer import BrushAlternateNamer
from sotd_collator.brush_name_extractor import BrushNameExtractor
from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.utils import timer_func


# Exports a CSV of match data for easier analysis
class MatchAnalyzer(object):
    LAST_MONTH = datetime.today().replace(day=1) - relativedelta(months=1)

    @timer_func
    def export_matches(
        self,
        extractor: BaseNameExtractor,
        renamer: BaseNameExtractor,
        target_month: datetime.date = LAST_MONTH,
    ):
        pr = praw.Reddit("reddit")
        pl = SotdPostLocator(pr)

        comments = pl.get_comments_for_given_month_staged(target_month)
        matches = []
        for comment in comments:
            entity_name = extractor.get_name(comment)
            if entity_name is not None:
                matches.append([entity_name, renamer.get_principal_name(entity_name)])

        path = (
            r"cache/analyzer/{extractor.__class__.__name__}/{renamer.__class__.__name__}"
        )
        if not os.path.exists(path):
            # if the demo_folder directory is not present
            # then create it.
            os.makedirs(path)

        month = (
            target_month.month if target_month.month >= 10 else f"0{target_month.month}"
        )

        file = f"{path}/{target_month.year}{month}.csv"

        with open(file, "w", encoding=sys.getdefaultencoding()) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["original", "match"])
            writer.writerows(matches)


if __name__ == "__main__":
    MatchAnalyzer().export_matches(BrushNameExtractor(), BrushAlternateNamer())
