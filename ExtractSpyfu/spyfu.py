import pandas as pd
import requests
import json
import time
import logging
from urllib.parse import urlparse
import numpy as np
import concurrent.futures
import datetime


def get_previous_month():
    today = datetime.date.today()
    if today.day > 10:
        previous_month = today.month - 1
        if previous_month == 0:
            previous_month = 12
    else:
        previous_month = today.month - 2
        if previous_month <= 0:
            previous_month += 12
    return previous_month


def last_month(secret_key, domain):
    try:
        params = {"domain": domain, "api_key": secret_key}
        previous_month = get_previous_month()
        current_year = datetime.date.today().year
        logging.info(f"Current Year: {current_year}")
        logging.info(f"Previous Month: {previous_month}")

        url = f"https://www.spyfu.com/apis/domain_stats_api/v2/getDomainStatsForExactDate?month={previous_month}&year={current_year}"

        raw_response = requests.get(url, params)
        logging.info("Spyfu status code:" + str(raw_response.status_code))

        response = json.loads(raw_response.content)
        logging.info("Spyfu response: " + str(response))

        stats_dict = response["results"][0]
        logging.info("Spyfu dict: " + str(stats_dict))

        final_dict = {
            "Site": domain,
            "spyfu_month": stats_dict.get("searchMonth"),
            "spyfu_year": stats_dict.get("searchYear"),
            "spyfu_last_month_avg_organic_rank": stats_dict.get("averageOrganicRank"),
            "spyfu_last_month_paid_clicks": stats_dict.get("monthlyPaidClicks"),
            "spyfu_last_month_avg_adrank": stats_dict.get("averageAdRank"),
            "spyfu_last_month_total_organic_results": stats_dict.get(
                "totalOrganicResults"
            ),
            "spyfu_last_month_budget": stats_dict.get("monthlyBudget"),
            "spyfu_last_month_organic_value": stats_dict.get("monthlyOrganicValue"),
            "spyfu_last_month_total_ads_purchased": stats_dict.get("totalAdsPurchased"),
            "spyfu_last_month_organic_clicks": stats_dict.get("monthlyOrganicClicks"),
            "spyfu_last_month_strength": stats_dict.get("strength"),
            "spyfu_last_month_tir": stats_dict.get("totalInverseRank"),
        }

        return final_dict
    except Exception as e:
        logging.error(f"ExtractSpyfu last_month func. error: {e}")
        logging.exception("")

        final_dict = {
            "Site": domain,
            "spyfu_month": "error",
            "spyfu_year": "error",
            "spyfu_last_month_avg_organic_rank": "error",
            "spyfu_last_month_paid_clicks": "error",
            "spyfu_last_month_avg_adrank": "error",
            "spyfu_last_month_total_organic_results": "error",
            "spyfu_last_month_budget": "error",
            "spyfu_last_month_organic_value": "error",
            "spyfu_last_month_total_ads_purchased": "error",
            "spyfu_last_month_organic_clicks": "error",
            "spyfu_last_month_strength": "error",
            "spyfu_last_month_tir": "error",
        }

        return final_dict


def avg_month(secret_key, domain, months=12):
    try:
        params = {"domain": domain, "api_key": secret_key}

        url = "https://www.spyfu.com/apis/domain_stats_api/v2/GetLatestDomainStats?month=3&year=2023"

        raw_response = requests.get(url, params)
        print(raw_response.status_code)

        response = json.loads(raw_response.content)

        monthly_list = response["results"]

        monthly_list = monthly_list[-months:]

        response = {}
        for i in monthly_list:
            for k, v in i.items():
                response[k] = response.get(k, 0) + int(v)

        for k, v in response.items():
            response[k] = v / 12 if v else 0

        final_dict = {
            "Site": domain,
            "spyfu_trailing_{}_avg_organic_rank": response.get("averageOrganicRank"),
            "spyfu_trailing_{}_avg_paid_clicks": response.get("monthlyPaidClicks"),
            "spyfu_trailing_{}_avg_adrank": response.get("averageAdRank"),
            "spyfu_trailing_{}_avg_total_organic_results": response.get(
                "totalOrganicResults"
            ),
            "spyfu_trailing_{}_avg_budget": response.get("monthlyBudget"),
            "spyfu_trailing_{}_avg_organic_value": response.get("monthlyOrganicValue"),
            "spyfu_trailing_{}_avg_total_ads_purchased": response.get(
                "totalAdsPurchased"
            ),
            "spyfu_trailing_{}_avg_organic_clicks": response.get(
                "monthlyOrganicClicks"
            ),
            "spyfu_trailing_{}_avg_strength": response.get("strength"),
            "spyfu_avg_kw_phrase_cpc": response.get("totalInverseRank"),
        }

        return final_dict

    except Exception as e:
        logging.error(f"ExtractSpyfu avg_month func. error: {e}")
        logging.exception("")

        final_dict = {
            "Site": domain,
            "spyfu_trailing_{}_avg_organic_rank": "error",
            "spyfu_trailing_{}_avg_paid_clicks": "error",
            "spyfu_trailing_{}_avg_adrank": "error",
            "spyfu_trailing_{}_avg_total_organic_results": "error",
            "spyfu_trailing_{}_avg_budget": "error",
            "spyfu_trailing_{}_avg_organic_value": "error",
            "spyfu_trailing_{}_avg_total_ads_purchased": "error",
            "spyfu_trailing_{}_avg_organic_clicks": "error",
            "spyfu_trailing_{}_avg_strength": "error",
            "spyfu_avg_kw_phrase_cpc": "error",
        }

        return final_dict


def avg_kw(secret_key, domain, kw_amount=5):
    try:
        params = {"query": domain, "api_key": secret_key, "pageSize": kw_amount}

        url = "https://www.spyfu.com/apis/keyword_api/v2/ppc/getMostSuccessful"

        raw_response = requests.get(url, params)
        print(raw_response.status_code)
        print(raw_response.content)
        response = json.loads(raw_response.content)
        print(response)
        monthly_list = response["results"]
        print(monthly_list)
        avg = len(monthly_list)

        response = {}
        for i in monthly_list:
            print(i)
            for k, v in i.items():
                try:
                    response[k] = response.get(k, 0) + int(v)
                except (ValueError, TypeError):
                    pass

        for k, v in response.items():
            try:
                response[k] = v / avg if v else 0
            except (ValueError, TypeError):
                pass

        print(response)

        final_dict = {
            "Site": domain,
            "spyfu_avg_kw_search_volume": response.get("searchVolume"),
            "spyfu_avg_kw_ranking_difficulty": response.get("rankingDifficulty"),
            "spyfu_avg_kw_monthly_clicks": response.get("totalMonthlyClicks"),
            "spyfu_avg_kw_searches_notclicked": response.get(
                "percentSearchesNotClicked"
            ),
            "spyfu_avg_kw_percent_organic_clicks": response.get("percentOrganicClicks"),
            "spyfu_avg_kw_broad_cpc": response.get("broadCostPerClick"),
            "spyfu_avg_kw_phrase_cpc": response.get("phraseCostPerClick"),
            "spyfu_avg_kw_exact_cpc": response.get("exactCostPerClick"),
            "spyfu_avg_kw_broad_clicks": response.get("broadMonthlyClicks"),
            "spyfu_avg_kw_phrase_clicks": response.get("phraseMonthlyClicks"),
            "spyfu_avg_kw_exact_clicks": response.get("exactMonthlyClicks"),
            "spyfu_avg_kw_broad_cost": response.get("broadMonthlyCost"),
            "spyfu_avg_kw_phrase_cost": response.get("phraseMonthlyCost"),
            "spyfu_avg_kw_exact_cost": response.get("exactMonthlyCost"),
            "spyfu_avg_kw_paid_competitors": response.get("paidCompetitors"),
            "spyfu_avg_kw_ranking_homepage": response.get("rankingHomepages"),
        }

        return final_dict

    except Exception as e:
        logging.error(f"ExtractSpyfu avg_kw func. error: {e}")
        logging.exception("")

        final_dict = {
            "Site": domain,
            "spyfu_avg_kw_search_volume": "error",
            "spyfu_avg_kw_ranking_difficulty": "error",
            "spyfu_avg_kw_monthly_clicks": "error",
            "spyfu_avg_kw_searches_notclicked": "error",
            "spyfu_avg_kw_percent_organic_clicks": "error",
            "spyfu_avg_kw_broad_cpc": "error",
            "spyfu_avg_kw_phrase_cpc": "error",
            "spyfu_avg_kw_exact_cpc": "error",
            "spyfu_avg_kw_broad_clicks": "error",
            "spyfu_avg_kw_phrase_clicks": "error",
            "spyfu_avg_kw_exact_clicks": "error",
            "spyfu_avg_kw_broad_cost": "error",
            "spyfu_avg_kw_phrase_cost": "error",
            "spyfu_avg_kw_exact_cost": "error",
            "spyfu_avg_kw_paid_competitors": "error",
            "spyfu_avg_kw_ranking_homepage": "error",
        }

        return final_dict


def get_competitors(secret_key, domain, organic=True, competitors=20):
    try:
        if organic:
            params = {
                "domain": domain,
                "api_key": secret_key,
                "isOrganic": "true",
                "r": competitors,
            }
        else:
            params = {
                "domain": domain,
                "api_key": secret_key,
                "isOrganic": "false",
                "r": competitors,
            }

        url = "https://www.spyfu.com/apis/core_api/get_domain_competitors_us"

        raw_response = requests.get(url, params)
        print(raw_response.status_code)

        response = json.loads(raw_response.content)

        ct_list = []

        for i in response:
            ct_list.append(i.get("domainName"))

        return ct_list
    except Exception as e:
        logging.exception("")
        logging.error(f"ExtractSpyfu get_competitors func. error: {e}")
        pass


def us_metrics(secret_key, domain):
    try:
        params = {
            "domain": domain,
            "api_key": secret_key,
        }

        url = "https://www.spyfu.com/apis/core_api/get_domain_metrics_us"

        raw_response = requests.get(url, params)
        print(raw_response.status_code)

        response = json.loads(raw_response.content)

        final_dict = {
            "Site": domain,
            "spyfu_avg_ad_position": response.get("avg_ad_position"),
            "spyfu_n_advertisers": response.get("number_of_advertisers"),
            "spyfu_num_paid_keywords": response.get("num_paid_keywords"),
            "spyfu_paid_clicks_permonth": response.get("paid_clicks_per_month"),
            "spyfu_n_organic_kw": response.get("num_organic_keywords"),
            "spyfu_organic_clicks_permonth": response.get("organic_clicks_per_month"),
            "spyfu_ads_daily_budget": response.get("daily_adwords_budget"),
            "spyfu_ads_monthly_budget": response.get("monthly_adwords_budget"),
            "spyfu_organic_daily_value": response.get("daily_organic_traffic_value"),
            "spyfu_organic_domain_rank": response.get("organic_domain_ranking"),
            "spyfu_paid_domain_rank": response.get("paid_domain_ranking"),
        }

        return final_dict
    except Exception as e:
        logging.error(f"ExtractSpyfu us_metrics func. error: {e}")
        logging.exception("")

        final_dict = {
            "Site": domain,
            "spyfu_avg_ad_position": "error",
            "spyfu_n_advertisers": "error",
            "spyfu_num_paid_keywords": "error",
            "spyfu_paid_clicks_permonth": "error",
            "spyfu_n_organic_kw": "error",
            "spyfu_organic_clicks_permonth": "error",
            "spyfu_ads_daily_budget": "error",
            "spyfu_ads_monthly_budget": "error",
            "spyfu_organic_daily_value": "error",
            "spyfu_organic_domain_rank": "error",
            "spyfu_paid_domain_rank": "error",
        }

        return final_dict


def spyfu(data_dict, config_dict):
    site_list = data_dict["site_list"]
    key = config_dict["key"]

    df = pd.DataFrame(site_list, columns=["Site"])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(last_month, key, row["Site"]) for _, row in df.iterrows()
        ]
        df1 = pd.DataFrame([future.result() for future in futures])

        futures = [
            executor.submit(avg_kw, key, row["Site"]) for _, row in df.iterrows()
        ]
        df2 = pd.DataFrame([future.result() for future in futures])

        futures = [
            executor.submit(us_metrics, key, row["Site"]) for _, row in df.iterrows()
        ]
        df3 = pd.DataFrame([future.result() for future in futures])

    ddfs = [
        df.set_index("Site"),
        df1.set_index("Site"),
        df2.set_index("Site"),
        df3.set_index("Site"),
    ]
    df = pd.concat(ddfs, axis=1)
    df = df.loc[:, ~df.columns.duplicated()]

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    for col in numeric_cols:
        df[col] = df[col].apply(lambda x: x if x > 0 else 0)
        df[col] = df[col].astype(np.float64, errors="ignore")

    return df
