import datetime
from dateutil.relativedelta import relativedelta

import inflect
import pandas as pd
import praw

from sotd_collator.blade_alternate_namer import BladeAlternateNamer
from sotd_collator.blade_format_extractor import BladeFormatExtractor
from sotd_collator.brush_alternate_namer import BrushAlternateNamer
from sotd_collator.karve_plate_extractor import KarvePlateExtractor
from sotd_collator.game_changer_plate_extractor import GameChangerPlateExtractor
from sotd_collator.knot_size_extractor import KnotSizeExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.razor_plus_blade_alternate_namer import RazorPlusBladeAlternateNamer
from sotd_collator.razor_plus_blade_name_extractor import RazorPlusBladeNameExtractor
from sotd_collator.sotd_post_locator import SotdPostLocator
from sotd_collator.staged_name_extractors import (
    StagedBladeNameExtractor,
    StagedBrushNameExtractor,
    StagedRazorNameExtractor,
    StagedUserNameExtractor,
)
from sotd_collator.superspeed_tip_extractor import SuperSpeedTipExtractor
from sotd_collator.utils import add_ranking_delta, get_shave_data, get_user_shave_data


class Runner(object):
    MAX_ENTITIES = 50

    def list_to_english_string(self, input_list):
        if not input_list:
            return ""

        if len(input_list) == 1:
            return input_list[0]
        
        if len(input_list) == 2:
            return f"{input_list[0]} and {input_list[1]}"

        # Join all elements except the last one with commas
        elements_except_last = ", ".join(input_list[:-1])

        # Combine the elements with commas and "and" for the last element
        result_string = f"{elements_except_last}, and {input_list[-1]}"

        return result_string


    def run(
        self,
        header: str,
        thread_map: dict,
        comments_target: [dict],
        comments_delta_one: [dict],
        comments_delta_two: [dict],
        delta_one_label: str,
        delta_two_label: str,
        min_shaves: int,
        min_unique_user: int,
        start_month: datetime.date,
        end_month: datetime.date,
    ):
        process_entities = [
            {
                "name": "Blade Format",
                "extractor": BladeFormatExtractor(),
                "renamer": None,
            },
            {
                "name": "Razor",
                "extractor": StagedRazorNameExtractor(),
                "renamer": RazorAlternateNamer(),
                "max_entities": 50,
            },
            {
                "name": "Blade",
                "extractor": StagedBladeNameExtractor(),
                "renamer": BladeAlternateNamer(),
                "max_entities": 50,
            },
            {
                "name": "Brush",
                "extractor": StagedBrushNameExtractor(),
                "renamer": BrushAlternateNamer(),
                "max_entites": 50,
            },
            {
                "name": "Knot Size",
                "extractor": KnotSizeExtractor(),
                "renamer": None,
            },
            {
                "name": "Karve Plate",
                "extractor": KarvePlateExtractor(),
                "renamer": None,
            },
            {
                "name": "Game Changer Plate",
                "extractor": GameChangerPlateExtractor(),
                "renamer": None,
            },
            {
                "name": "Superspeed Tip",
                "extractor": SuperSpeedTipExtractor(),
                "renamer": None,
            },
        ]

        inf_engine = inflect.engine()

        print(header)
        razor_usage = None
        for entity in process_entities:
            print(f"##{inf_engine.plural(entity['name'])}\n")

            # print(f'retrieving {target_label} usage', end='\r')
            usage = get_shave_data(
                thread_map, comments_target, entity["extractor"], entity["renamer"]
            )
            # print(f'retrieving {delta_one_label} usage', end='\r')
            pm_usage = get_shave_data(
                thread_map, comments_delta_one, entity["extractor"], entity["renamer"]
            )
            # print(f'retrieving {delta_two_label} usage', end='\r')
            py_usage = get_shave_data(
                thread_map, comments_delta_two, entity["extractor"], entity["renamer"]
            )

            # print(f'adding {delta_one_label} delta', end='\r')
            usage = add_ranking_delta(usage, pm_usage, delta_one_label)
            # print(f'adding {delta_two_label} delta', end='\r')
            usage = add_ranking_delta(usage, py_usage, delta_two_label)
            # print(f'dropping rank', end='\r')
            usage.drop("rank", inplace=True, axis=1)

            # remove nulls
            # print('removing nulls', end='\r')
            usage.dropna(subset=["name"], inplace=True)

            # sort
            # print('sorting', end='\r')
            usage.sort_values(["shaves", "unique users"], ascending=False, inplace=True)

            # enforce max entities
            # print('enforcing max entities', end='\r')
            max_entities = (
                entity["max_entities"]
                if "max_entities" in entity
                else self.MAX_ENTITIES
            )
            usage = usage.head(max_entities)

            print(usage.to_markdown(index=False))
            print("\n")

            if isinstance(entity["extractor"], StagedRazorNameExtractor):
                razor_usage = usage

        print("## Most Used Blades in Most Used Razors\n")

        # do razor plus blade combo, filtered on most popular razors...
        # razor_usage = get_shave_data(comments_target, RazorNameExtractor(), RazorAlternateNamer())
        rpb_usage = get_shave_data(
            thread_map,
            comments_target,
            RazorPlusBladeNameExtractor(),
            RazorPlusBladeAlternateNamer(),
        )
        razor_usage.sort_values(
            ["shaves", "unique users"], ascending=False, inplace=True
        )

        # get most popular razors in use this month
        top_x_razors = razor_usage.head(10).loc[:, ["name"]]
        top_x_razors.columns = ["razor_name"]

        # extract razor name from combined razor + blades df
        rpb_usage.loc[:, "razor_name"] = rpb_usage["name"].apply(
            lambda x: x.split("+")[0].strip()
        )
        rpb_usage.sort_values(["shaves", "unique users"], ascending=False, inplace=True)

        rpb_usage = pd.merge(
            left=rpb_usage, right=top_x_razors, on="razor_name", how="inner"
        ).drop(["rank", "razor_name"], axis=1)

        rpb_usage = (
            rpb_usage.where(rpb_usage["shaves"] >= min_shaves)
            .where(rpb_usage["unique users"] >= min_unique_user)
            .dropna()
        )

        print(rpb_usage.to_markdown(index=False))
        print("\n")

        usage = self.top_shavers(
            thread_map,
            comments_target,
            comments_delta_one,
            comments_delta_two,
            delta_one_label,
            delta_two_label,
            start_month,
            end_month
        )

        print("## Top Shavers\n")
        print(usage.to_markdown(index=False))

        print("\n")

    def top_shavers(
        self,
        thread_map,
        comments_target,
        comments_delta_one,
        comments_delta_two,
        delta_one_label,
        delta_two_label,
        start_month,
        end_month
    ):

        # usage = get_shave_data(thread_map, comments_target, StagedUserNameExtractor(), None)
        pm_usage = get_shave_data(thread_map, comments_delta_one, StagedUserNameExtractor(), None)
        py_usage = get_shave_data(thread_map, comments_delta_two, StagedUserNameExtractor(), None)
        usage = get_user_shave_data(thread_map, comments_target, StagedUserNameExtractor(), start_month, end_month)
        usage = add_ranking_delta(usage, pm_usage, delta_one_label)
        usage = add_ranking_delta(usage, py_usage, delta_two_label)
        usage.drop("rank", inplace=True, axis=1)
        usage.drop("unique users", inplace=True, axis=1)
        usage.drop("avg shaves per user", inplace=True, axis=1)

        # remove nulls
        usage.dropna(subset=["name"], inplace=True)

        # sort
        usage.sort_values(["shaves"], ascending=False, inplace=True)
        head = 0
        last = 0
        # curr_month = datetime.strptime(comments_target[0]["created_utc"], "%Y-%m-%d %H:%M:%S")
        # days_in_month = (calendar.monthrange(curr_month.year, curr_month.month)[1])
        for index, row in usage.iterrows():
            head += 1
            if head >= 20 and row["shaves"] < last:
                break
            last = row["shaves"]

        usage = usage.head(head)
        usage.rename(columns={"name": "user"}, inplace=True)
        return usage

    # print('## Shaving Frequency Histogram\n')
    # print(get_shaving_histogram(stats_month, pl).to_markdown(index=False))
    # print('\n')


if __name__ == "__main__":
    pr = praw.Reddit("reddit")
    pl = SotdPostLocator(pr)

    target = datetime.date.today().replace(day=1) - relativedelta(months=1)
    last_month = target - relativedelta(months=1)
    last_year = target - relativedelta(years=1)

    comments_target = pl.get_comments_for_given_month_staged(target)
    comments_last_month = pl.get_comments_for_given_month_staged(last_month)
    comments_last_year = pl.get_comments_for_given_month_staged(last_year)

    target_label = target.strftime("%B %Y")
    last_month_label = last_month.strftime("%b %Y")
    last_year_label = last_year.strftime("%b %Y")

    usage = Runner().top_shavers(
        comments_target,
        comments_last_month,
        comments_last_year,
        last_month_label,
        last_year_label,
    )
    print("## Top Contributors\n")
    print(usage.to_markdown(index=True))

    print("\n")
