# shared functions and the like
import pandas as pd
from calendar import monthrange
from base_alternate_namer import BaseAlternateNamer
from base_name_extractor import BaseNameExtractor


def get_shave_data(comments: [dict], name_extractor: BaseNameExtractor, alternate_namer: BaseAlternateNamer, name_fallback=True):
    # pull comments and user ids from reddit, generate per-entity dataframe with shaves, unique users
    raw_usage = {'name': [], 'user_id': []}

    for comment in comments:
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

            raw_usage['name'].append(principal_name)
            raw_usage['user_id'].append(comment["author"])

    df = pd.DataFrame(raw_usage)
    df = df.groupby('name').agg({"user_id": ['count', 'nunique']}).reset_index()
    df.columns = ['name', 'shaves', 'unique users']
    df = df[df.apply(lambda x: x['name'].lower() != 'none', axis=1)]
    df.loc[:, 'avg shaves per user'] = df.apply(lambda x: '{0:.2f}'.format(x['shaves'] / x['unique users'] if x['unique users'] > 0 else 0), axis=1)
    df.loc[:, 'rank'] = df['shaves'].rank(method='dense', ascending=False)
    return df

def get_shave_data_for_month(given_month, post_locator, name_extractor, alternate_namer, name_fallback=True):
    comments = post_locator.get_comments_for_given_month_cached(given_month)
    return get_shave_data(comments, name_extractor, alternate_namer, name_fallback)

def get_shave_data_for_year(given_year, post_locator, name_extractor, alternate_namer, name_fallback=True):
    comments = post_locator.get_comments_for_given_year_cached(given_year)
    return get_shave_data(comments, name_extractor, alternate_namer, name_fallback)

def get_shaving_histogram(given_month, post_locator):
    # pull comments and user ids from reddit, generate per-entity dataframe with shaves, unique users
    # note this is not 100% accurate - if a user posts twice in the same sotd thread we cant prevent double counting that
    raw_usage = {'user_id': []}

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
        raw_usage['user_id'].extend(list(users_for_day))

    df = pd.DataFrame(raw_usage)
    df = df.groupby('user_id').size().reset_index()
    df.columns = ['user_id', 'shaves']
    df.loc[:, 'shaves'] = df['shaves'].apply(_enforce_max_shaves)
    df = df.groupby(['shaves']).agg({'user_id': 'nunique'}).reset_index()
    df.columns = ['#shaves', 'number of users who shaved this many times this month']
    df.sort_values(['#shaves'], ascending=False, inplace=True)
    return df

def get_entity_histogram(given_month, post_locator, name_extractor, alternate_namer, entity_title):
    # get number of users who used 1, 2, 3, n razors / brushes / etc per month
    raw_usage = {'name': [], 'user_id': []}
    entity_title = '#' + entity_title

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

            raw_usage['name'].append(principal_name)
            raw_usage['user_id'].append(comment["author"])

    df = pd.DataFrame(raw_usage)
    df = df.groupby('user_id').agg({'name': 'nunique'}).reset_index()
    df.columns = ['user_id', entity_title]
    df = df.groupby([entity_title]).agg({'user_id': 'nunique'}).reset_index()
    df.columns = [entity_title, 'number of users who used this many {0} this month'.format(entity_title[1:].lower())]
    df.sort_values([entity_title], inplace=True)
    return df


def add_ranking_delta(df_curr, df_prev, historic_name):
    # enrich the current data frame with the delta in rank from the historic dataframe

    def _get_delta(row):
        if pd.isnull(row['previous_rank']):
            # ie not seen last period
            return 'n/a'
        elif row['rank'] == row['previous_rank']:
            return '='
        elif row['rank'] < row['previous_rank']:
            # need to specifically make this an int otherwise pandas considers it a float and shows as eg ^1.0
            return '↑{0}'.format(int(row['previous_rank'] - row['rank']))
        elif row['rank'] > row['previous_rank']:
            return '↓{0}'.format(int(row['rank'] - row['previous_rank']))

    df_prev = df_prev[['name', 'rank']]
    df_prev.columns = ['name', 'previous_rank']

    df_curr = pd.merge(
        left=df_curr,
        right=df_prev,
        on='name',
        how='left',
    )
    df_curr.loc[:, 'Δ vs {0}'.format(historic_name)] = df_curr.apply(_get_delta, axis=1)
    df_curr.drop('previous_rank', inplace=True, axis=1)

    return df_curr


def get_unlinked_entity_data(comments: [dict], name_extractor, alternate_namer):
    # all the cases where we cant match a razor / brush / etc as posted by the user
    raw_unlinked = {'name': [], 'user_id': []}

    for comment in comments:
        entity_name = name_extractor.get_name(comment)
        if entity_name is not None:
            principal_name = None
            if alternate_namer:
                principal_name = alternate_namer.get_principal_name(entity_name)
            if not principal_name:
                raw_unlinked['name'].append(entity_name)
                raw_unlinked['user_id'].append(comment["author"])

    df = pd.DataFrame(raw_unlinked)
    df = df.groupby('name').agg({"user_id": ['count', 'nunique']}).reset_index()
    df.columns = ['name', 'shaves', 'unique users']
    df = df[df.apply(lambda x: x['name'].lower() != 'none', axis=1)]
    return df
