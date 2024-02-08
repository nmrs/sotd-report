# shared functions and the like
from concurrent.futures import thread
from datetime import datetime, date
import re
from time import time
import pandas as pd
from calendar import calendar, monthrange
from base_alternate_namer import BaseAlternateNamer
from base_name_extractor import BaseNameExtractor


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
        return result

    return wrap_func


def get_shave_data(
    thread_map,
    comments: [dict],
    name_extractor: BaseNameExtractor,
    alternate_namer: BaseAlternateNamer,
    name_fallback=True,
):
    # pull comments and user ids from reddit, generate per-entity dataframe with shaves, unique users
    raw_usage = get_raw_data(thread_map, comments, name_extractor, alternate_namer, name_fallback)

    df = pd.DataFrame(raw_usage)
    df = df.groupby("name").agg({"user_id": ["count", "nunique"]}).reset_index()
    df.columns = ["name", "shaves", "unique users"]
    df = df[df.apply(lambda x: x["name"].lower() != "none", axis=1)]
    df.loc[:, "avg shaves per user"] = df.apply(
        lambda x: "{0:.2f}".format(
            x["shaves"] / x["unique users"] if x["unique users"] > 0 else 0
        ),
        axis=1,
    )
    df.loc[:, "rank"] = df["shaves"].rank(method="dense", ascending=False)
    return df

def get_user_shave_data(
    thread_map: dict,
    comments: [dict],
    name_extractor: BaseNameExtractor,
    start_month: datetime.date,
    end_month: datetime.date
):
    # pull comments and user ids from reddit, generate per-entity dataframe with shaves, unique users
    raw_usage = get_raw_data(thread_map, comments, name_extractor, None, True)
    raw_df = pd.DataFrame(raw_usage)
    raw_df['date'] = pd.to_datetime(raw_df['date'])

    start_day = start_month.replace(day=1)
    days_in_month = monthrange(end_month.year, end_month.month)[1]
    end_day = end_month.replace(day=days_in_month)

    # Create a DataFrame with all days of the month for each user
    date_range = pd.date_range(start_day, end_day, freq='D')
    users = raw_df['name'].unique()
    date_user_df = pd.DataFrame([(date, user) for date in date_range for user in users], columns=['date', 'name'])
    # Merge the original DataFrame with the new one
    merged_df = pd.merge(date_user_df, raw_df, on=['date', 'name'], how='left')
    # Filter out days where no comments were made
    no_comment_days = merged_df[merged_df['user_id'].isnull()]

    # Count the number of days without comments for each user
    missed_days = no_comment_days.groupby('name')['date'].count()
    missed_days.name = "missed days"

    shave_df = get_shave_data(thread_map, comments, name_extractor, None, True)

    result = shave_df.merge(missed_days, on="name")
    return result


def get_raw_data(thread_map, comments, name_extractor, alternate_namer, name_fallback):

    raw_usage = {"name": [], "user_id": [], "date": []}

    for comment in comments:
        thread_id = extract_thread_id_from_comment_url(comment['url'])
        thread_date = extract_date_from_thread_title(thread_map[thread_id]["title"])
        entity_name = name_extractor.get_name(comment)
        if entity_name is not None:
            principal_name = None
            if alternate_namer:
                principal_name = alternate_namer.get_principal_name(entity_name)
            if not principal_name:
                if not name_fallback:
                    # skip this one if we dont want to fall back to the base entity name
                    continue
                else:
                    # no renamer or no principal name found, so avoid nulls and use raw entity name
                    principal_name = entity_name

            raw_usage["name"].append(principal_name)
            raw_usage["user_id"].append(comment["author"])
            raw_usage["date"].append(thread_date)
    return raw_usage


def get_shave_data_for_month(
    given_month, post_locator, name_extractor, alternate_namer, name_fallback=True
):
    comments = post_locator.get_comments_for_given_month_cached(given_month)
    return get_shave_data(comments, name_extractor, alternate_namer, name_fallback)


def get_shave_data_for_year(
    given_year, post_locator, name_extractor, alternate_namer, name_fallback=True
):
    comments = post_locator.get_comments_for_given_year_cached(given_year)
    return get_shave_data(comments, name_extractor, alternate_namer, name_fallback)


def get_shaving_histogram(given_month, post_locator):
    # pull comments and user ids from reddit, generate per-entity dataframe with shaves, unique users
    # note this is not 100% accurate - if a user posts twice in the same sotd thread we cant prevent double counting that
    raw_usage = {"user_id": []}

    def _enforce_max_shaves(shaves):
        # because we can over count if people post twice in a given thread, limit max shaves to num days in month
        days_in_month = monthrange(given_month.year, given_month.month)[1]
        if shaves > days_in_month:
            shaves = days_in_month
        return shaves

    for comment in post_locator.get_comments_for_given_month_cached(given_month):
        users_for_day = set()
        if comment["author"]:
            users_for_day.add(comment["author"])
        raw_usage["user_id"].extend(list(users_for_day))

    df = pd.DataFrame(raw_usage)
    df = df.groupby("user_id").size().reset_index()
    df.columns = ["user_id", "shaves"]
    df.loc[:, "shaves"] = df["shaves"].apply(_enforce_max_shaves)
    df = df.groupby(["shaves"]).agg({"user_id": "nunique"}).reset_index()
    df.columns = ["#shaves", "number of users who shaved this many times this month"]
    df.sort_values(["#shaves"], ascending=False, inplace=True)
    return df


def get_entity_histogram(
    given_month, post_locator, name_extractor, alternate_namer, entity_title
):
    # get number of users who used 1, 2, 3, n razors / brushes / etc per month
    raw_usage = {"name": [], "user_id": []}
    entity_title = "#" + entity_title

    for comment in post_locator.get_comments_for_given_month_cached(given_month):
        entity_name = name_extractor.get_name(comment)
        if not comment["author"]:
            continue

        if entity_name is not None:
            principal_name = None
            if alternate_namer:
                principal_name = alternate_namer.get_principal_name(entity_name)
            if not principal_name:
                # no renamer or no principal name found, so avoid nulls and use raw entity name
                principal_name = entity_name

            raw_usage["name"].append(principal_name)
            raw_usage["user_id"].append(comment["author"])

    df = pd.DataFrame(raw_usage)
    df = df.groupby("user_id").agg({"name": "nunique"}).reset_index()
    df.columns = ["user_id", entity_title]
    df = df.groupby([entity_title]).agg({"user_id": "nunique"}).reset_index()
    df.columns = [
        entity_title,
        "number of users who used this many {0} this month".format(
            entity_title[1:].lower()
        ),
    ]
    df.sort_values([entity_title], inplace=True)
    return df


def add_ranking_delta(df_curr, df_prev, historic_name):
    # enrich the current data frame with the delta in rank from the historic dataframe

    def _get_delta(row):
        if pd.isnull(row["previous_rank"]):
            # ie not seen last period
            return "n/a"
        elif row["rank"] == row["previous_rank"]:
            return "="
        elif row["rank"] < row["previous_rank"]:
            # need to specifically make this an int otherwise pandas considers it a float and shows as eg ^1.0
            return "↑{0}".format(int(row["previous_rank"] - row["rank"]))
        elif row["rank"] > row["previous_rank"]:
            return "↓{0}".format(int(row["rank"] - row["previous_rank"]))

    df_prev = df_prev[["name", "rank"]]
    df_prev.columns = ["name", "previous_rank"]

    df_curr = pd.merge(
        left=df_curr,
        right=df_prev,
        on="name",
        how="left",
    )
    df_curr.loc[:, "Δ vs {0}".format(historic_name)] = df_curr.apply(_get_delta, axis=1)
    df_curr.drop("previous_rank", inplace=True, axis=1)

    return df_curr


def get_unlinked_entity_data(comments: [dict], name_extractor, alternate_namer):
    # all the cases where we cant match a razor / brush / etc as posted by the user
    raw_unlinked = {"name": [], "user_id": []}

    for comment in comments:
        entity_name = name_extractor.get_name(comment)
        if entity_name is not None:
            principal_name = None
            if alternate_namer:
                principal_name = alternate_namer.get_principal_name(entity_name)
            if not principal_name:
                raw_unlinked["name"].append(entity_name)
                raw_unlinked["user_id"].append(comment["author"])

    df = pd.DataFrame(raw_unlinked)
    df = df.groupby("name").agg({"user_id": ["count", "nunique"]}).reset_index()
    df.columns = ["name", "shaves", "unique users"]
    df = df[df.apply(lambda x: x["name"].lower() != "none", axis=1)]
    return df

def extract_date_from_thread_title(title):
    # Define a regular expression pattern for matching dates with variations in spacing
    # date_pattern = re.compile(r'.*(\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?).*\s+\d{1,2}\s*,?\s*\d{4})')
    date_patterns = [
        r".*(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*\s+\d{1,2}\s*,?\s*\d{4})",
        r".*(\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*,?\s+\d{4})",
    ]

    date_formats = ["%b %d, %Y", "%B %d, %Y", "%b. %d, %Y", "%b %d %Y", "%d %b %Y"]

    replacements = [(r'\b(\d{2})\b', r'\1'), (r'\b(\d{1})\b', r'0\1')]

    for pattern in date_patterns:
        # regex = re.compile(pattern)

        # Search for the pattern in the input string
        match = re.search(pattern, title)

        if match:
            for format in date_formats:
                for replacement in replacements:
                    date_string = re.sub(replacement[0], replacement[1], match.group(1))
                    try:
                        date_obj = datetime.strptime(date_string, format).date()
                        return date_obj
                    except ValueError:
                        pass

    raise ValueError(f"Unable to extract date from: {title}")

def extract_thread_id_from_comment_url(url):
    pattern = re.compile(r'/comments/([^/]+)/')
    match = pattern.search(url)

    if match:
        return match.group(1)
    raise ValueError(f"Unable to find thread id in {url}")
        