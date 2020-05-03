import datetime
from pprint import pprint
import inflect
import pandas as pd

import praw
from dateutil.relativedelta import relativedelta

from sotd_collator.blade_alternate_namer import BladeAlternateNamer
from sotd_collator.blade_name_extractor import BladeNameExtractor
from sotd_collator.brush_alternate_namer import BrushAlternateNamer
from sotd_collator.brush_name_extractor import BrushNameExtractor
from sotd_collator.knot_size_extractor import KnotSizeExtractor
from sotd_collator.razor_name_extractor import RazorNameExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.utils import add_ranking_delta, get_shave_data_for_month

pr = praw.Reddit('standard_creds', user_agent='arach')
pl = SotdPostLocator(pr)
inf_engine = inflect.engine()

# only report entities with >= this many shaves
MIN_SHAVES = 3



process_entities = [
    {
        'name': 'Razor',
        'extractor': RazorNameExtractor(),
        'renamer': RazorAlternateNamer(),
    },
    {
        'name': 'Blade',
        'extractor': BladeNameExtractor(),
        'renamer': BladeAlternateNamer(),
    },
    {
        'name': 'Brush',
        'extractor': BrushNameExtractor(),
        'renamer': BrushAlternateNamer(),
    },
    {
        'name': 'Knot Size',
        'extractor': KnotSizeExtractor(),
        'renamer': None,
    },
]

stats_month = datetime.date(2020,4,1)
previous_month = stats_month - relativedelta(months=1)
previous_year = stats_month - relativedelta(months=12)

for entity in process_entities:

    usage = get_shave_data_for_month(stats_month, pl, entity['extractor'], entity['renamer'])
    pm_usage = get_shave_data_for_month(previous_month, pl, entity['extractor'], entity['renamer'])

    usage = add_ranking_delta(usage, pm_usage, previous_month.strftime('%b %Y'))
    usage = add_ranking_delta(usage, pm_usage, previous_year.strftime('%b %Y'))
    usage.drop('rank', inplace=True, axis=1)

    # enforce min shaves
    usage = usage.where(usage['shaves'] >= MIN_SHAVES)

    # remove nulls
    usage.dropna(subset=['name'], inplace=True)

    # sort
    usage.sort_values('shaves', ascending=False, inplace=True)

    print('##{0}\n'.format(inf_engine.plural(entity['name'])))

    print(usage.to_markdown(showindex=False))
    print('\n')
