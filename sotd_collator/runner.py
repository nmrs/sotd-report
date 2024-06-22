import datetime
from typing import List
from dateutil.relativedelta import relativedelta

import inflect
import pandas as pd
import praw
from blackbird_plate_parser import BlackbirdPlateParser
import blade_name_extractor
from blade_parser import BladeParser
from brush_handle_parser import BrushHandleParser
from brush_parser import BrushParser
from game_changer_plate_parser import GameChangerPlateParser
from karve_plate_parser import KarvePlateParser
from razor_parser import RazorParser
from razor_plus_blade_parser import RazorPlusBladeParser

from razor_format_extractor import RazorFormatExtractor
from razor_plus_blade_name_extractor import RazorPlusBladeNameExtractor
from sotd_post_locator import SotdPostLocator
from staged_name_extractors import (
    StagedBladeNameExtractor,
    StagedBladeUseExtractor,
    StagedBrushNameExtractor,
    StagedRazorNameExtractor,
    StagedUserNameExtractor,
)
from straight_parsers import (
    StraightGrindParser,
    StraightPointParser,
    StraightWidthParser,
)
from utils import (
    add_ranking_delta,
    get_raw_data_from_parser,
    get_shave_data_from_parser,
    get_user_shave_data,
    single_user_report,
)
from superspeed_tip_parser import SuperSpeedTipParser


class Runner(object):
    MAX_ENTITIES = 50
    MIN_SHAVES = 1

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
        comments_target: List[dict],
        comments_delta_one: List[dict],
        comments_delta_two: List[dict],
        comments_delta_three: List[dict],
        delta_one_label: str,
        delta_two_label: str,
        delta_three_label: str,
        min_shaves: int,
        min_unique_user: int,
        start_month: datetime.date,
        end_month: datetime.date,
    ):
        rne = StagedRazorNameExtractor()
        bne = StagedBladeNameExtractor()
        brne = StagedBrushNameExtractor()

        rp = RazorParser()
        blp = BladeParser()
        brp = BrushParser()
        bfe = RazorFormatExtractor(bne, blp, rne, rp)
        kpp = KarvePlateParser(rp)
        gcp = GameChangerPlateParser(rp)
        sstp = SuperSpeedTipParser(rp)
        process_entities = [
            {
                "name": "Razor Format",
                "extractor": bfe,
                "min_shaves": 1,
            },
            {
                "name": "Razor",
                "extractor": rne,
                "parser": rp,
                "parser field": "name",
                "max_entities": 50,
            },
            {
                "name": "Razor Manufacturer",
                "extractor": rne,
                "parser": rp,
                "parser field": "brand",
                "min_shaves": 10,
            },
            {
                "name": "Blade",
                "extractor": bne,
                "parser": blp,
                "parser field": "name",
                "max_entities": 50,
            },
            {
                "name": "Brush",
                "extractor": brne,
                "parser": brp,
                "parser field": "name",
                "max_entites": 50,
                "fallback": True,
            },
            {
                "name": "Brush Handle Maker",
                "extractor": brne,
                "parser": BrushHandleParser(),
                "parser field": "name",
                "min_shaves": 10,
            },
            {
                "name": "Brush Knot Maker",
                "extractor": brne,
                "parser": brp,
                "parser field": "knot maker",
                "min_shaves": 10,
            },
            {
                "name": "Knot Fiber",
                "extractor": brne,
                "parser": brp,
                "parser field": "fiber",
                "max_entites": 50,
                "fallback": False,
            },
            {
                "name": "Knot Size",
                "extractor": brne,
                "parser": brp,
                "parser field": "knot size",
                "max_entites": 50,
                "fallback": False,
            },
            {
                "name": "Blackbird Plate",
                "extractor": rne,
                "parser": BlackbirdPlateParser(rp),
                "parser field": "name",
                "fallback": False,
            },
            {
                "name": "Christopher Bradley Plate",
                "extractor": rne,
                "parser": kpp,
                "parser field": "name",
                "fallback": False,
            },
            {
                "name": "Game Changer Plate",
                "extractor": rne,
                "parser": gcp,
                "parser field": "name",
                "fallback": False,
            },
            {
                "name": "Straight Width",
                "extractor": rne,
                "parser": StraightWidthParser(rp),
                "parser field": "name",
                "fallback": False,
            },
            {
                "name": "Straight Grind",
                "extractor": rne,
                "parser": StraightGrindParser(rp),
                "parser field": "name",
                "fallback": False,
            },
            {
                "name": "Straight Point",
                "extractor": rne,
                "parser": StraightPointParser(rp),
                "parser field": "name",
                "fallback": False,
            },
            # {
            #     "name": "Super Speed Tip",
            #     "extractor": rne,
            #     "parser": sstp,
            #     "parser field": "name",
            #     "fallback": False,
            # },
        ]

        inf_engine = inflect.engine()

        print(header)
        razor_usage = None
        for entity in process_entities:
            print(f"##{inf_engine.plural(entity['name'])}\n")

            usage = self.entity_usage(
                thread_map,
                comments_target,
                comments_delta_one,
                comments_delta_two,
                comments_delta_three,
                delta_one_label,
                delta_two_label,
                delta_three_label,
                entity,
            )

            print(usage.to_markdown(index=False))
            print("\n")

            if entity["name"] == "Razor":
                razor_usage = usage

        print("## Most Used Blades in Most Used Razors\n")

        # do razor plus blade combo, filtered on most popular razors...
        # razor_usage = get_shave_data(comments_target, RazorNameExtractor(), RazorAlternateNamer())
        # bpr_usage = self.blade_per_razor(
        #     thread_map,
        #     comments_target,
        #     min_shaves,
        #     min_unique_user,
        #     rp,
        #     blp,
        #     razor_usage,
        # )

        # print(bpr_usage.to_markdown(index=False))
        print("\n")

        usage = self.blade_heroes(
            thread_map,
            comments_target,
            comments_delta_one,
            comments_delta_two,
            comments_delta_three,
            delta_one_label,
            delta_two_label,
            delta_three_label,
            start_month,
            end_month,
            bne,
            blp,
            bfe,
        )

        print("## Highest Use Count per Blade\n")
        print(usage.to_markdown(index=False))
        print("\n")

        usage = self.top_shavers(
            thread_map,
            comments_target,
            comments_delta_one,
            comments_delta_two,
            comments_delta_three,
            delta_one_label,
            delta_two_label,
            delta_three_label,
            start_month,
            end_month,
        )

        print("## Top Shavers\n")
        print(usage.to_markdown(index=False))
        print("\n")

    def entity_usage(
        self,
        thread_map,
        comments_target,
        comments_delta_one,
        comments_delta_two,
        comments_delta_three,
        delta_one_label,
        delta_two_label,
        delta_three_label,
        entity,
    ):
        extractor = entity["extractor"]
        parser = entity["parser"] if "parser" in entity else None
        parser_field = entity["parser field"] if "parser field" in entity else None
        fallback = entity["fallback"] if "fallback" in entity else True

        # print(f'retrieving {target_label} usage', end='\r')
        usage = get_shave_data_from_parser(
            thread_map,
            comments_target,
            extractor,
            parser,
            parser_field,
            fallback,
        )
        # print(f'retrieving {delta_one_label} usage', end='\r')
        d1_usage = get_shave_data_from_parser(
            thread_map,
            comments_delta_one,
            extractor,
            parser,
            parser_field,
            fallback,
        )
        # print(f'retrieving {delta_two_label} usage', end='\r')
        d2_usage = get_shave_data_from_parser(
            thread_map,
            comments_delta_two,
            extractor,
            parser,
            parser_field,
            fallback,
        )

        d3_usage = None
        if comments_delta_three is not None:
            d3_usage = get_shave_data_from_parser(
                thread_map,
                comments_delta_three,
                extractor,
                parser,
                parser_field,
                fallback,
            )

            # print(f'adding {delta_one_label} delta', end='\r')
        usage = add_ranking_delta(usage, d1_usage, delta_one_label)
        # print(f'adding {delta_two_label} delta', end='\r')
        usage = add_ranking_delta(usage, d2_usage, delta_two_label)

        if d3_usage is not None:
            usage = add_ranking_delta(usage, d3_usage, delta_three_label)

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
            entity["max_entities"] if "max_entities" in entity else self.MAX_ENTITIES
        )
        usage = usage.head(max_entities)

        min_shaves = entity["min_shaves"] if "min_shaves" in entity else self.MIN_SHAVES
        usage = usage[usage["shaves"] >= min_shaves]
        return usage

    def blade_per_razor(
        self,
        thread_map,
        comments_target,
        min_shaves,
        min_unique_user,
        rp,
        blp,
        razor_usage,
    ):
        rpb_usage = get_shave_data_from_parser(
            thread_map,
            comments_target,
            RazorPlusBladeNameExtractor(),
            RazorPlusBladeParser(rp, blp),
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

        return rpb_usage

    def top_shavers(
        self,
        thread_map,
        comments_target,
        comments_delta_one,
        comments_delta_two,
        comments_delta_three,
        delta_one_label,
        delta_two_label,
        delta_three_label,
        start_month,
        end_month,
    ):

        # usage = get_shave_data(thread_map, comments_target, StagedUserNameExtractor(), None)
        d1_usage = get_shave_data_from_parser(
            thread_map, comments_delta_one, StagedUserNameExtractor(), None
        )
        d2_usage = get_shave_data_from_parser(
            thread_map, comments_delta_two, StagedUserNameExtractor(), None
        )

        d3_usage = None
        if comments_delta_three is not None:
            d3_usage = get_shave_data_from_parser(
                thread_map, comments_delta_three, StagedUserNameExtractor(), None
            )

        usage = get_user_shave_data(
            thread_map,
            comments_target,
            StagedUserNameExtractor(),
            start_month,
            end_month,
        )
        usage = add_ranking_delta(usage, d1_usage, delta_one_label)
        usage = add_ranking_delta(usage, d2_usage, delta_two_label)
        if d3_usage is not None:
            usage = add_ranking_delta(usage, d3_usage, delta_three_label)
        usage.drop("rank", inplace=True, axis=1)
        usage.drop("unique users", inplace=True, axis=1)
        usage.drop("avg shaves per user", inplace=True, axis=1)

        # remove nulls
        usage.dropna(subset=["name"], inplace=True)

        # sort
        usage["name lower"] = usage.loc[:, "name"].str.lower()
        usage = usage.sort_values(
            ["shaves", "missed days", "name lower"],
            ascending=[False, True, True],
            ignore_index=True,
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
            if head >= 20 and row["shaves"] <= last:
                if len(all_rows) > head:
                    next_row = all_rows[head + 1]
                    if row["shaves"] > next_row["shaves"]:
                        break
                    elif row["shaves"] == next_row["shaves"]:
                        if row["missed days"] < next_row["missed days"]:
                            break

            last = row["shaves"]
        usage = usage.head(head + 1)
        usage.drop("name lower", inplace=True, axis=1)

        usage.rename(columns={"name": "user"}, inplace=True)
        return usage

    # print('## Shaving Frequency Histogram\n')
    # print(get_shaving_histogram(stats_month, pl).to_markdown(index=False))
    # print('\n')

    def blade_heroes(
        self,
        thread_map,
        comments_target,
        comments_delta_one,
        comments_delta_two,
        comments_delta_three,
        delta_one_label,
        delta_two_label,
        delta_three_label,
        start_month,
        end_month,
        bne: blade_name_extractor.BladeNameExtractor,
        bp: BladeParser,
        bfe: RazorFormatExtractor,
    ):
        raw_blade_count = get_raw_data_from_parser(
            thread_map, comments_target, StagedBladeUseExtractor(), None
        )
        raw_blade_count_df = pd.DataFrame(raw_blade_count)
        raw_blade_count_df.rename(columns={"name": "uses"}, inplace=True)
        raw_blade_count_df["uses"] = raw_blade_count_df["uses"].apply(int)
        raw_blade_count_df.drop(
            ["body", "original", "matched", "date"], inplace=True, axis=1
        )

        raw_blade_usage = get_raw_data_from_parser(thread_map, comments_target, bne, bp)
        raw_blade_usage_df = pd.DataFrame(raw_blade_usage)
        raw_blade_usage_df.rename(columns={"name": "blade"}, inplace=True)
        raw_blade_usage_df.drop(
            ["body", "original", "matched", "date"], inplace=True, axis=1
        )

        raw_format_usage = get_raw_data_from_parser(
            thread_map, comments_target, bne, bp, "format", None
        )
        raw_format_usage_df = pd.DataFrame(raw_format_usage)
        raw_format_usage_df.rename(columns={"name": "format"}, inplace=True)
        raw_format_usage_df.drop(
            ["body", "original", "matched", "date"], inplace=True, axis=1
        )

        raw_merged_df = pd.merge(
            raw_blade_count_df, raw_blade_usage_df, on=["url", "user_id"], how="inner"
        )
        raw_merged_df = pd.merge(
            raw_merged_df, raw_format_usage_df, on=["url", "user_id"], how="inner"
        )
        raw_merged_df.drop("url", inplace=True, axis=1)
        # raw_merged_df.drop("body", inplace=True, axis=1)

        raw_merged_df2 = (
            raw_merged_df.groupby(["blade", "format"])["uses"].max().reset_index()
        )

        raw_merged_df3 = pd.merge(
            raw_merged_df, raw_merged_df2, on=["blade", "format", "uses"], how="inner"
        ).sort_values(["uses"], ascending=False)

        df = raw_merged_df3[raw_merged_df3["uses"] >= 30]

        # raw_merged_df2 = (
        #     raw_merged_df.groupby("uses")[["user_id", "blade", "format"]]
        #     .max()
        #     .reset_index()
        # )

        # de_df = raw_merged_df3[raw_merged_df3["format"] == "DE"]
        # de_df = de_df.sort_values(["uses", "blade"], ascending=False)
        # de_df2 = de_df[de_df["uses"] >= 30]

        # gem_df = raw_merged_df3[raw_merged_df3["format"] == "GEM"]
        # gem_df = gem_df.sort_values(["uses", "blade"], ascending=False)
        # gem_df2 = gem_df[gem_df["uses"] >= 30]

        # df = pd.concat([de_df2, gem_df2]).sort_values(
        #     ["uses", "format"], ascending=[False, True]
        # )

        df2 = df.copy()
        df2["user"] = df["user_id"].apply(lambda x: f"u/{x}")
        df3 = df2.drop(["user_id"], axis=1)
        df4 = df3[["user", "blade", "format", "uses"]]
        return df4


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

    thread_map = pl.get_thread_map(target, target)
    dt = single_user_report(
        "u/tsrblke",
        comments_target,
        thread_map,
        StagedUserNameExtractor(),
        target,
        target,
    )

    print(dt.to_markdown())

    # usage = Runner().top_shavers(
    #     comments_target,
    #     comments_last_month,
    #     comments_last_year,
    #     last_month_label,
    #     last_year_label,
    # )
    # print("## Top Contributors\n")
    # print(usage.to_markdown(index=True))

    print("\n")
