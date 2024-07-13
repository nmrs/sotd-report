import datetime
from typing import List
from dateutil.relativedelta import relativedelta

import inflect
import pandas as pd
import praw

from soap_name_extractor import SoapNameExtractor
from soap_parser import SoapParser
from sotd_post_locator import SotdPostLocator
from staged_name_extractors import (
    StagedSoapNameExtractor,
    StagedUserNameExtractor,
)
from utils import (
    add_ranking_delta,
    get_raw_data_from_parser,
    get_shave_data_from_parser,
    get_user_shave_data,
    single_user_report,
)
from superspeed_tip_parser import SuperSpeedTipParser


class SoapRunner(object):
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
        sne = StagedSoapNameExtractor()

        snp = SoapParser()

        process_entities = [
            {
                "name": "Soap Maker",
                "extractor": sne,
                "parser": snp,
                "parser field": "brand",
                "min_shaves": 5,
                "max_entities": 150,
            },
            {
                "name": "Soap",
                "extractor": sne,
                "parser": snp,
                "parser field": "name",
                "min_shaves": 5,
                "max_entities": 150,
            },
            # {
            #     "name": "Format",
            #     "extractor": sne,
            #     "parser": snp,
            #     "parser field": "format",
            #     "min_shaves": 1,
            #     "max_entities": 150,
            #     "fallback": False,
            # },
        ]

        inf_engine = inflect.engine()

        print(header)
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

        usage = self.brand_diversity(
            thread_map,
            comments_target,
            comments_delta_one,
            comments_delta_two,
            comments_delta_three,
            delta_one_label,
            delta_two_label,
            delta_three_label,
            sne,
            snp,
            5,
        )

        print("## Brand Diversity\n")
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
        max_entities = (
            entity["max_entities"] if "max_entities" in entity else self.MAX_ENTITIES
        )
        min_shaves = entity["min_shaves"] if "min_shaves" in entity else self.MIN_SHAVES

        # print(f'retrieving {target_label} usage', end='\r')
        usage = self.usage_for_field(
            thread_map,
            comments_target,
            comments_delta_one,
            comments_delta_two,
            comments_delta_three,
            delta_one_label,
            delta_two_label,
            delta_three_label,
            extractor,
            parser,
            parser_field,
            fallback,
        )

        # enforce max entities
        # print('enforcing max entities', end='\r')
        usage = usage.head(max_entities)

        usage = usage[usage["shaves"] >= min_shaves]
        return usage

    def usage_for_field(
        self,
        thread_map,
        comments_target,
        comments_delta_one,
        comments_delta_two,
        comments_delta_three,
        delta_one_label,
        delta_two_label,
        delta_three_label,
        extractor,
        parser,
        parser_field,
        fallback,
    ):
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
        return usage

    def brand_diversity(
        self,
        thread_map,
        comments_target,
        comments_delta_one,
        comments_delta_two,
        comments_delta_three,
        delta_one_label,
        delta_two_label,
        delta_three_label,
        extractor: SoapNameExtractor,
        parser: SoapParser,
        min_scents=5,
    ):

        # print(f'retrieving {target_label} usage', end='\r')
        usage = self.period_brand_diversity(
            thread_map, comments_target, extractor, parser
        )
        d1_usage = self.period_brand_diversity(
            thread_map, comments_delta_one, extractor, parser
        )
        d2_usage = self.period_brand_diversity(
            thread_map, comments_delta_two, extractor, parser
        )
        d3_usage = None
        if comments_delta_three is not None:
            d3_usage = self.period_brand_diversity(
                thread_map, comments_delta_three, extractor, parser
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
        usage = usage[usage["unique scents"] >= min_scents]
        return usage

    def period_brand_diversity(self, thread_map, comments_target, extractor, parser):
        usage = get_raw_data_from_parser(
            thread_map,
            comments_target,
            extractor,
            parser,
            "brand",
            False,
        )
        df = pd.DataFrame(usage)
        df = df.drop(["matched", "body"], axis=1)
        df = df.rename(columns={"name": "brand"})

        u2 = get_raw_data_from_parser(
            thread_map,
            comments_target,
            extractor,
            parser,
            "name",
            False,
        )

        df2 = pd.DataFrame(u2)
        df2 = df2.drop(["matched", "body"], axis=1)

        df = pd.merge(df, df2, on=["user_id", "url", "original", "date"], how="left")
        df = df.groupby("brand").agg({"name": ["count", "nunique"]}).reset_index()
        df.columns = ["name", "shaves", "unique scents"]
        df = df[["name", "unique scents", "shaves"]]
        df = df[df.apply(lambda x: x["name"].lower() != "none", axis=1)]
        df.loc[:, "avg shaves per scent"] = df.apply(
            lambda x: "{0:.2f}".format(
                x["shaves"] / x["unique scents"] if x["unique scents"] > 0 else 0
            ),
            axis=1,
        )
        df.loc[:, "rank"] = df["unique scents"].rank(method="dense", ascending=False)
        # return df

        df.sort_values(["unique scents", "shaves"], ascending=False, inplace=True)
        return df

        # # print(f'retrieving {delta_one_label} usage', end='\r')
        # d1_usage = get_shave_data_from_parser(
        #     thread_map,
        #     comments_delta_one,
        #     extractor,
        #     parser,
        #     parser_field,
        #     fallback,
        # )
        # # print(f'retrieving {delta_two_label} usage', end='\r')
        # d2_usage = get_shave_data_from_parser(
        #     thread_map,
        #     comments_delta_two,
        #     extractor,
        #     parser,
        #     parser_field,
        #     fallback,
        # )

        # d3_usage = None
        # if comments_delta_three is not None:
        #     d3_usage = get_shave_data_from_parser(
        #         thread_map,
        #         comments_delta_three,
        #         extractor,
        #         parser,
        #         parser_field,
        #         fallback,
        #     )

        #     # print(f'adding {delta_one_label} delta', end='\r')
        # usage = add_ranking_delta(usage, d1_usage, delta_one_label)
        # # print(f'adding {delta_two_label} delta', end='\r')
        # usage = add_ranking_delta(usage, d2_usage, delta_two_label)

        # if d3_usage is not None:
        #     usage = add_ranking_delta(usage, d3_usage, delta_three_label)

        #     # print(f'dropping rank', end='\r')
        # usage.drop("rank", inplace=True, axis=1)

        # # remove nulls
        # # print('removing nulls', end='\r')
        # usage.dropna(subset=["name"], inplace=True)

        # # sort
        # # print('sorting', end='\r')
        # usage.sort_values(["shaves", "unique users"], ascending=False, inplace=True)

        # # enforce max entities
        # # print('enforcing max entities', end='\r')
        # max_entities = (
        #     entity["max_entities"] if "max_entities" in entity else self.MAX_ENTITIES
        # )
        # usage = usage.head(max_entities)

        # min_shaves = entity["min_shaves"] if "min_shaves" in entity else self.MIN_SHAVES
        # usage = usage[usage["shaves"] >= min_shaves]
        # return usage

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
        "u/Engineered_Shave",
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
