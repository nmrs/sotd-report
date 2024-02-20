import datetime
from typing import List
from dateutil.relativedelta import relativedelta

import inflect
import pandas as pd
import praw
from blade_parser import BladeParser
from brush_parser import BrushParser
from razor_parser import RazorParser

from sotd_post_locator import SotdPostLocator
from staged_name_extractors import (
    StagedBladeNameExtractor,
    StagedBrushNameExtractor,
    StagedRazorNameExtractor,
    StagedUserNameExtractor,
)
from utils import (
    get_raw_data_from_parser,
    get_user_shave_data,
)


class DebugRunner(object):

    def run(
        self, thread_map: dict, comments_target: List[dict], start_month, end_month
    ):
        rne = StagedRazorNameExtractor()
        bne = StagedBladeNameExtractor()

        rp = RazorParser()
        blp = BladeParser()
        brp = BrushParser()

        process_entities = [
            # {
            #     "name": "Blade Format",
            #     "extractor": BladeFormatExtractor(bne, blp, rne, rp),
            # },
            {
                "name": "Razor",
                "extractor": rne,
                "parser": rp,
                "parser field": "name",
            },
            # {
            #     "name": "Razor Manufacturer",
            #     "extractor": rne,
            #     "parser": rp,
            #     "parser field": "brand",
            # },
            # {
            #     "name": "Blade",
            #     "extractor": bne,
            #     "parser": blp,
            #     "parser field": "name",
            # },
            # {
            #     "name": "Brush",
            #     "extractor": StagedBrushNameExtractor(),
            #     "parser": brp,
            #     "parser field": "name",
            #     "fallback": True,
            # },
            # {
            #     "name": "Fiber",
            #     "extractor": StagedBrushNameExtractor(),
            #     "parser": brp,
            #     "parser field": "fiber",
            #     "fallback": False,
            # },
            # {
            #     "name": "Knot Size",
            #     "extractor": StagedBrushNameExtractor(),
            #     "parser": brp,
            #     "parser field": "knot size",
            #     "fallback": False,
            # },
            # {
            #     "name": "Karve Plate",
            #     "extractor": KarvePlateExtractor(),
            # },
            # {
            #     "name": "Game Changer Plate",
            #     "extractor": GameChangerPlateExtractor(),
            # },
            # {
            #     "name": "Superspeed Tip",
            #     "extractor": SuperSpeedTipExtractor(),
            # },
        ]

        inf_engine = inflect.engine()

        # for entity in process_entities:
        #     self.process_entity(thread_map, comments_target, blp, inf_engine, entity)

        self.process_user_shave_data(
            thread_map, comments_target, start_month, end_month
        )
        return

    def process_entity(self, thread_map, comments_target, blp, inf_engine, entity):
        print(f"##{inf_engine.plural(entity['name'])}\n")

        extractor = entity["extractor"]
        parser = entity["parser"] if "parser" in entity else None
        parser_field = entity["parser field"] if "parser field" in entity else None
        fallback = entity["fallback"] if "fallback" in entity else True

        # print(f'retrieving {target_label} usage', end='\r')
        raw_usage = get_raw_data_from_parser(
            thread_map, comments_target, extractor, parser, parser_field, fallback
        )
        df_raw = pd.DataFrame(raw_usage)
        df_raw["original"] = df_raw["original"].apply(
            lambda x: blp.remove_digits_in_parens(x)
        )
        df = df_raw.drop("user_id", inplace=False, axis=1)
        df = df.drop("date", inplace=False, axis=1)
        df = df.drop("url", inplace=False, axis=1)
        # df = df.groupby(["name", "original"]).agg(count=("original", "count"))
        # df = df.groupby(["name", "original"])[["original"]].agg("count")
        df_counts = df.value_counts(["name"]).reset_index(name="a")
        df = df.value_counts(["name", "original", "matched"]).reset_index(name="b")
        df_unique = df.value_counts(["name", "original"]).reset_index(name="b")
        df = df.merge(df_counts, how="left")
        df["name"] = df["name"].str[:50]
        # df = df.value_counts(["name"]).reset_index(name="c")
        df = df.sort_values(
            ["a", "matched", "name", "b"], ascending=[False, False, True, False]
        )
        print(df.to_markdown(index=False))
        print("\n")

    def process_user_shave_data(
        self, thread_map, comments_target, start_month, end_month
    ):
        print("Top Shavers")
        # usage = get_shave_data(thread_map, comments_target, StagedUserNameExtractor(), None)

        usage = get_user_shave_data(
            thread_map,
            comments_target,
            StagedUserNameExtractor(),
            start_month,
            end_month,
        )

        usage.drop("rank", inplace=True, axis=1)
        usage.drop("unique users", inplace=True, axis=1)
        usage.drop("avg shaves per user", inplace=True, axis=1)

        # remove nulls
        usage.dropna(subset=["name"], inplace=True)

        # sort
        usage["name lower"] = usage.loc[:, "name"].str.lower()
        usage = usage.sort_values(
            ["shaves", "missed days", "name lower"], ascending=[False, True, True]
        )
        head = 0
        last = 0
        # curr_month = datetime.strptime(comments_target[0]["created_utc"], "%Y-%m-%d %H:%M:%S")
        # days_in_month = (calendar.monthrange(curr_month.year, curr_month.month)[1])
        all_rows = []
        for index, row in usage.iterrows():
            all_rows.append(row)

        for row in all_rows:
            head += 1
            if head >= 21 and row["shaves"] <= last:
                if len(all_rows) > head:
                    next_row = all_rows[head + 1]
                    if row["shaves"] > next_row["shaves"]:
                        break
                    elif row["shaves"] == next_row["shaves"]:
                        if row["missed days"] < next_row["missed days"]:
                            break

            last = row["shaves"]
        usage = usage.head(head)
        usage.drop("name lower", inplace=True, axis=1)

        usage.rename(columns={"name": "user"}, inplace=True)
        print(usage.to_markdown(index=False))


if __name__ == "__main__":
    pr = praw.Reddit("reddit")
    pl = SotdPostLocator(pr)

    # target = datetime.date.today().replace(day=1) - relativedelta(months=1)
    # end_month = target

    target = datetime.date(2023, 1, 1)
    end_month = datetime.date(2023, 12, 1)

    comments_target = []
    thread_map = {}
    curr_month = target
    while curr_month <= end_month:
        comments_target = comments_target + pl.get_comments_for_given_month_staged(
            curr_month
        )
        thread_map = thread_map | pl.get_thread_map(curr_month, curr_month)
        curr_month = curr_month + relativedelta(months=1)

    DebugRunner().run(thread_map, comments_target, target, end_month)
    # usage = Runner().top_shavers(
    #     comments_target,
    #     comments_last_month,
    #     comments_last_year,
    #     last_month_label,
    #     last_year_label,
    # )
    # print("## Top Contributors\n")
    # print(usage.to_markdown(index=True))

    # print("\n")