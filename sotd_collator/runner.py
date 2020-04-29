import datetime
from pprint import pprint

import praw
from dateutil.relativedelta import relativedelta

from sotd_collator.blade_alternate_namer import BladeAlternateNamer
from sotd_collator.blade_name_extractor import BladeNameExtractor
from sotd_collator.brush_alternate_namer import BrushAlternateNamer
from sotd_collator.brush_name_extractor import BrushNameExtractor
from sotd_collator.razor_name_extractor import RazorNameExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.utils import get_ranked_datastructure, get_ranking_delta, get_shave_data_for_month

pr = praw.Reddit('standard_creds', user_agent='arach')
pl = SotdPostLocator(pr)

# only report entities with >= this many shaves
MIN_SHAVES = 3



process_entities = [
    # {
    #     'name': 'Razor',
    #     'extractor': RazorNameExtractor(),
    #     'renamer': RazorAlternateNamer(),
    # },
    {
        'name': 'Blade',
        'extractor': BladeNameExtractor(),
        'renamer': BladeAlternateNamer(),
    },
    # {
    #     'name': 'Brush',
    #     'extractor': BrushNameExtractor(),
    #     'renamer': BrushAlternateNamer(),
    # },
]

stats_month = datetime.date(2019,5,1)
previous_month = stats_month - relativedelta(months=1)

for entity in process_entities:

    usage, total_shaves = get_shave_data_for_month(stats_month, pl, entity['extractor'], entity['renamer'])
    # get previous month's stats for position changes
    pm_usage, pm_total_shaves = get_shave_data_for_month(previous_month, pl, entity['extractor'], entity['renamer'])

    print('|{0}|Shaves in {1}|% of all shaves in {1}|Change in rank vs prev month|'.format(
        *[
            entity['name'],
            stats_month.strftime('%b %Y')
        ]
    ))

    pprint(get_ranked_datastructure(usage))
    pprint(get_ranked_datastructure(pm_usage))
    pprint(pm_usage)
    print('|---|---|---|---|')
    for razor_name, num_shaves in sorted(usage.items(), key=lambda item: item[1], reverse=True):
        if num_shaves < MIN_SHAVES:
            continue
        print('|{0}|{1}|{2:0.2f}|{3}|'.format(
            *[
                razor_name,
                num_shaves,
                num_shaves * 100.0 / total_shaves,
                get_ranking_delta(razor_name, get_ranked_datastructure(usage), get_ranked_datastructure(pm_usage))
            ]))

    print('\n\n')
