# shared functions and the like
from collections import defaultdict


def get_shave_data_for_month(given_month, post_locator, name_extractor, alternate_namer):
    raw_usage = defaultdict(int)
    clustered_usage = defaultdict(int)

    for comment in post_locator.get_comments_for_given_month_cached(given_month):
        entity_name = name_extractor.get_name(comment)
        if entity_name is not None:
            raw_usage[entity_name] += 1

    total_shaves_for_month = 0

    for entity_name, uses in raw_usage.items():
        if not entity_name:
            continue
        principal_name = alternate_namer.get_principal_name(entity_name)
        if principal_name:
            clustered_usage[principal_name] += uses
        else:
            # avoid nulls
            clustered_usage[entity_name] += uses
        total_shaves_for_month += uses

    return clustered_usage, total_shaves_for_month


def get_ranked_datastructure(usage_data):
    # compare - generate ranked datastructures
    # cant simply sort and enumerate, because at the lower end we have many razors with the same number of shaves
    # ie many razors share the same rank

    # convert shaves to ranks
    rank_mapper = {shaves: rank + 1 for rank, shaves in enumerate(
        sorted(
            {x: 1 for x in usage_data.values()}.keys(), # ie unique list of number of shaves
            reverse=True,
        )
    )}

    return {razor: rank_mapper[shaves] for razor, shaves in usage_data.items()}


def get_ranking_delta(entity_name, ranked, ranked_prev_month):
    if not entity_name in ranked_prev_month:
        # ie not seen last month
        return 'n/a'
    elif ranked[entity_name] == ranked_prev_month[entity_name]:
        return '='
    elif ranked[entity_name] < ranked_prev_month[entity_name]:
        return '↑{0}'.format(ranked_prev_month[entity_name] - ranked[entity_name])
    elif ranked[entity_name] > ranked_prev_month[entity_name]:
        return '↓{0}'.format(ranked[entity_name] - ranked_prev_month[entity_name])