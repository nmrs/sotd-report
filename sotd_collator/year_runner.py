import datetime
from pprint import pprint

import praw
from dateutil.relativedelta import relativedelta


from sotd_collator.runner import Runner
from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.stage_builder import StageBuilder
from sotd_collator.utils import add_ranking_delta, get_shave_data, get_shave_data_for_month, get_shaving_histogram, get_entity_histogram

pr = praw.Reddit('reddit')
pl = SotdPostLocator(pr)

target = 2023
last_year = target - 1
five_years_ago = target - 5

sb = StageBuilder()
sb.build_stage(datetime.date(last_year, 1, 1), datetime.date(target, 12, 31))
sb.build_stage(datetime.date(five_years_ago, 1, 1), datetime.date(five_years_ago, 12, 31))

comments_target = pl.get_comments_for_given_year_staged(target)
comments_last_year = pl.get_comments_for_given_year_staged(last_year)
comments_five_years_ago = pl.get_comments_for_given_year_staged(five_years_ago)

target_label = str(target)
last_year_label = str(last_year)
five_years_ago_label = str(five_years_ago)

header = (f"""
Welcome to your SOTD Hardware Report for {target_label}

## Observations

* A fairly nondescript month


## Notes & Caveats

* I only show the top n results per category to keep the tables readable and avoid max post length issues.

* Blade Format stats dont differentiate between DE and half DE razors, they are all counted as being DE blades

* Any brush with a DG knot will come under the DG Bx category - eg Dogwood B8 is recorded as 'DG B8'

* In the case of most brush makers (eg Maggard) - knots are split into synthetic / badger / boar and attributed to the maker - eg 'Maggard Synthetic'

* Notable exceptions to this are Omega and Semogue, in order to retain the model number. Unless some jerk just puts 'Omega Boar' which I then report as 'Omega Boar (model not specified)' .

* The unique user column shows the number of different users who used a given razor / brush etc in the month. We can combine this with the total number of shaves to get the average number of times a user used a razor / brush etc

* The change Δ vs columns show how an item has moved up or down the rankings since the previous month or year. = means no change in position, up or down arrows indicate how many positions up or down the rankings an item has moved compared to the previous month or year. n/a means the item was not present in the previous month / year.

""")

runner = Runner()
runner.run( header, comments_target, comments_last_year,
            comments_five_years_ago, last_year_label, five_years_ago_label )