from random import randint
from .searchData import get_company_id_by_url
import pandas as pd


def build_graph_dict(scores, type_score):

    evolution_score_list = []

    for companies in scores:
        temp = {}
        for key, value in companies.items():
            if value is None:
                value = 0
            if key == type_score:
                temp[key] = value
            if key == "initial_date":
                temp[key] = value.strftime("%Y-%m")
        evolution_score_list.append(temp)

    df = pd.DataFrame(evolution_score_list)
    df.drop_duplicates(subset=['initial_date'], keep='last', inplace=True)
    evolution_score_list = df.to_dict("records")

    return evolution_score_list


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def add_https_to_urls(competitors):
    competitors_https = []
    VAR_HTTPS = 'https://'
    for competitor in competitors:
        if 'https://' in competitor:
            competitors_https.append(competitor)
        else:
            competitor = VAR_HTTPS + competitor
            competitor = competitor.lower()
            competitors_https.append(competitor)
    return competitors_https


def add_competitors_to_dict(competitors, project_dict):
    pos = 1
    for competitor in competitors:
        key = "competitor_" + str(pos)
        project_dict[key] = get_company_id_by_url(
            competitor)
        pos += 1
    return project_dict
