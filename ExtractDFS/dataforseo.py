import pandas as pd
import tldextract
import multiprocessing.dummy as mp
import logging
from http.client import HTTPSConnection
from base64 import b64encode
from json import loads
from json import dumps
import requests
import os

import numpy as np
from shared_code.storage_functions import AzureStorage


class RestClient:
    domain = "api.dataforseo.com"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)
        try:
            base64_bytes = b64encode(
                ("%s:%s" % (self.username, self.password)).encode("ascii")
            ).decode("ascii")
            headers = {
                "X-RapidAPI-Key": "9c33b473demsh0fd262e6ed2a3f0p1ab63cjsn8e3f12e367ad",
                "X-RapidAPI-Host": "similar-web.p.rapidapi.com",
            }
            connection.request(method, path, headers=headers, body=data)
            response = connection.getresponse()
            return loads(response.read().decode())
        finally:
            connection.close()

    def get(self, path):
        return self.request(path, "GET")

    def post(self, path, data):
        if isinstance(data, str):
            data_str = data
        else:
            data_str = dumps(data)
        return self.request(path, "POST", data_str)


# add backlinks request
def backlinks_metrics(domain, client):
    try:
        url = "https://api.dataforseo.com/v3/backlinks/summary/live"

        payload = (
            '[{"target":"%s", "internal_list_limit":10, "backlinks_status_type":"live", "include_subdomains":true}]'
            % (domain)
        )
        headers = {
            "Authorization": "Basic a2VlbmZvbGtzZGlnaXRhbEBnbWFpbC5jb206OThkY2EzNjM2NmMzMzRmYg==",
            "Content-Type": "application/json",
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        logging.info(
            "Requesting backlinks and referring domains from Dataforseo",
            extra={"domain": domain, "client": client},
        )
        return response.json()
    except Exception as e:
        logging.error(f"DFS metrics Function: {e}")


# add check status code
def check_status_code(domain, client, attempt=0):
    try:
        response = backlinks_metrics(domain, client)
        status_code = response["tasks"][0]["status_code"]
        status_message = response["tasks"][0]["status_message"]
        # Full list of the response codes here https://docs.dataforseo.com/v3/appendix/errors
        if status_code == 20000:
            logging.info(
                f"Successful request {client} for {domain} from Dataforseo",
                extra={"domain": domain, "client": client},
            )
            try:
                result_dict = response["tasks"][0]["result"][0]
                return result_dict
            except:
                logging.error(
                    "Failed request {client} for {domain} from Dataforseo",
                    exc_info=True,
                )
                pass
        elif status_code == 40501:
            logging.error(
                f"Dataforseo No Target Error while processing {client} for {domain}",
                extra={"domain": domain, "client": client},
            )
            return

        # The rate-limit per minute has been exceeded, sleep for 60 secs
        elif status_code == 40202:
            logging.info(
                f"Dataforseo Rate Limite Error, sleep for 60 secs",
                extra={"domain": domain, "client": client},
            )
            return check_status_code(domain, client)
        else:
            logging.error(
                "Failed request Dataforseo",
                exc_info=True,
                extra={
                    "status_code": status_code,
                    "status_message": status_message,
                    "domain": domain,
                    "client": client,
                },
            )
            return "ok"
    except Exception:
        logging.error("Failed request Dataforseo", exc_info=True)
        return "not ok"


def dataframe_generator_backlinks(site, domain, result_dict):
    # Creating Dataframe and extracting required metrics:

    data = pd.DataFrame(index=[domain])
    data["Site"] = site
    try:
        data["Totalbacklinks"] = result_dict["backlinks"]
    except:
        data["Totalbacklinks"] = 0
    try:
        data["Referringdomains"] = result_dict["referring_main_domains"]
    except:
        data["Referringdomains"] = 0
    try:
        data["WebAuthority"] = result_dict["rank"]
    except:
        data["WebAuthority"] = 0
    logging.info(f"{domain} backlinks dataframe generated")
    return data


import datetime


def calculate_previous_month_dates():
    current_date = datetime.date.today()
    previous_month_end_date = current_date.replace(day=1) - datetime.timedelta(days=1)
    previous_month_start_date = previous_month_end_date.replace(day=1)

    # Format the previous month's end date as "YYYY-MM"
    previous_month_end_date_formatted = previous_month_end_date.strftime("%Y-%m")

    # Calculate the start dates of the previous 12 months
    previous_12_month_start_dates = []
    for i in range(1, 13):
        month = previous_month_start_date.month - i
        year = previous_month_start_date.year
        if month <= 0:
            month += 12
            year -= 1
        previous_12_month_start_dates.append(
            datetime.date(year, month, 1).strftime("%Y-%m")
        )

    return previous_month_end_date_formatted, previous_12_month_start_dates


def rapid_api_metrics(domain):
    try:
        # Test the function
        (
            previous_month_end_date,
            previous_12_month_start_dates,
        ) = calculate_previous_month_dates()
        date_list = []
        for start_date in previous_12_month_start_dates:
            date_list.append(start_date)
        # Check if the current date is after the 10th of the month

        from datetime import datetime

        current_date = datetime.now()
        if current_date.day > 10:
            start_date = min(date_list)
            end_date = previous_month_end_date
            logging.info(
                f"If current date is more than 10th then start and end date: {start_date,end_date}"
            )
        else:
            start_date = min(date_list)
            end_date = max(date_list)
            logging.info(
                f"If current date is less than 10th then start and end date: {start_date,end_date}"
            )

        api_key = os.getenv("SIMILARWEB_API_KEY")
        global_rank = f"https://api.similarweb.com/v1/website/{domain}/global-rank/global-rank?api_key={api_key}"
        country_lead_rank_countrywiserankandtraffic = f"https://api.similarweb.com/v4/website/{domain}/geo/traffic-by-country?api_key={api_key}"
        category = f"https://api.similarweb.com/v1/website/{domain}/category-rank/category-rank?api_key={api_key}"
        montly_traffic = f"https://api.similarweb.com/v1/website/{domain}/total-traffic-and-engagement/visits?api_key={api_key}&start_date={start_date}&end_date={end_date}&country=world&granularity=monthly&main_domain_only=false&format=json&show_verified=false&mtd=false"
        avg_time_onsite = f"https://api.similarweb.com/v1/website/{domain}/total-traffic-and-engagement/average-visit-duration?api_key={api_key}&start_date={start_date}&end_date={end_date}&country=world&granularity=monthly&main_domain_only=false&format=json&show_verified=false&mtd=false"
        avg_pageview = f"https://api.similarweb.com/v1/website/{domain}/total-traffic-and-engagement/pages-per-visit?api_key={api_key}&start_date={start_date}&end_date={end_date}&country=world&granularity=monthly&main_domain_only=false&format=json&show_verified=false&mtd=false"
        bounce_rate = f"https://api.similarweb.com/v1/website/{domain}/total-traffic-and-engagement/bounce-rate?api_key={api_key}&start_date={start_date}&end_date={end_date}&country=world&granularity=monthly&main_domain_only=false&format=json&show_verified=false&mtd=false"
        traffic_overview = f"https://api.similarweb.com/v1/website/{domain}/traffic-sources/overview-share?api_key={api_key}&start_date={start_date}&end_date={end_date}&country=world&granularity=monthly&main_domain_only=false&format=json&show_verified=false&mtd=false"

        headers = {"accept": "application/json"}

        global_rank = requests.get(global_rank, headers=headers).json()
        country_lead_rank_countrywiserankandtraffic = requests.get(
            country_lead_rank_countrywiserankandtraffic, headers=headers
        ).json()
        category_result = requests.get(category, headers=headers).json()
        avg_time_onsite = requests.get(avg_time_onsite, headers=headers).json()
        avg_pageview = requests.get(avg_pageview, headers=headers).json()
        bounce_rate = requests.get(bounce_rate, headers=headers).json()
        traffic_overview = requests.get(traffic_overview, headers=headers).json()
        montly_traffic = requests.get(montly_traffic, headers=headers).json()
        try:
            global_rank = global_rank.get("global_rank")[0]["global_rank"]
        except:
            global_rank = 0
        try:
            country_rank = country_lead_rank_countrywiserankandtraffic.get("records")[
                0
            ]["rank"]
        except:
            country_rank = 0
        try:
            lead_country = country_lead_rank_countrywiserankandtraffic.get("records")[
                0
            ]["country"]
        except:
            lead_country = 0
        try:
            category = category_result.get("category")
        except:
            category = 0
        try:
            category_rank = category_result.get("rank")
        except:
            category_rank = 0
        try:
            monthly_traffic_result = montly_traffic.get("visits")
        except:
            monthly_traffic_result = 0
        try:
            avg_time = avg_time_onsite.get("average_visit_duration")
        except:
            avg_time = 0
        try:
            page_per_view_result = avg_pageview.get("pages_per_visit")
        except:
            page_per_view_result = 0
        try:
            bouncerate = bounce_rate.get("bounce_rate")
        except:
            bouncerate = 0

        try:
            original_data = traffic_overview.get("visits")[domain]
        except:
            original_data = 0
        try:
            sorted_list = country_lead_rank_countrywiserankandtraffic.get("records")
            lenght = len(sorted_list)
            top_5 = sorted_list[:lenght]
        except:
            top_5 = 0
        try:
            top_country1 = top_5[0]["country"]
        except:
            top_country1 = 0
        try:
            top_country1_pct = top_5[0]["visits"]
        except:
            top_country1_pct = 0
        try:
            top_country2 = top_5[1]["country"]
        except:
            top_country2 = 0
        try:
            top_country2_pct = top_5[1]["visits"]
        except:
            top_country2_pct = 0
        try:
            top_country3 = top_5[2]["country"]
        except:
            top_country3 = 0
        try:
            top_country3_pct = top_5[2]["visits"]
        except:
            top_country3_pct = 0
        try:
            top_country4 = top_5[3]["country"]
        except:
            top_country4 = 0
        try:
            top_country4_pct = top_5[3]["visits"]
        except:
            top_country4_pct = 0
        try:
            top_country5 = top_5[4]["country"]
        except:
            top_country5 = 0
        try:
            top_country5_pct = top_5[4]["visits"]
        except:
            top_country5_pct = 0

        output = {
            "global_rank": global_rank,
            "country_rank": country_rank,
            "lead_country": lead_country,
            "category": category,
            "category_rank": category_rank,
            "top_country1": top_country1,
            "top_country1_pct": top_country1_pct,
            "top_country2": top_country2,
            "top_country2_pct": top_country2_pct,
            "top_country3": top_country3,
            "top_country3_pct": top_country3_pct,
            "top_country4": top_country4,
            "top_country4_pct": top_country4_pct,
            "top_country5": top_country5,
            "top_country5_pct": top_country5_pct,
        }

        result = {}

        for item in original_data:
            for visit in item["visits"]:
                if visit["date"] not in result:
                    result[visit["date"]] = {"date": visit["date"]}
                result[visit["date"]][item["source_type"]] = visit

        # add values from monthly_traffic_result
        for visit in monthly_traffic_result:
            date = visit["date"]
            if date not in result:
                result[date] = {"date": date}
            result[date]["monthly_traffic"] = visit["visits"]
        for visit in avg_time:
            date = visit["date"]
            if date not in result:
                result[date] = {"date": date}
            result[date]["average_visit_duration"] = visit["average_visit_duration"]
        # add values from page_per_view_result
        for visit in page_per_view_result:
            date = visit["date"]
            if date not in result:
                result[date] = {"date": date}
            result[date]["pages_per_visit"] = visit["pages_per_visit"]

        for visit in bouncerate:
            date = visit["date"]
            if date not in result:
                result[date] = {"date": date}
            result[date]["bounce_rate"] = visit["bounce_rate"]
        # add values from data
        for item in original_data:
            for visit in item["visits"]:
                date = visit["date"]
                if date not in result:
                    result[date] = {"date": date}
                if item["source_type"] not in result[date]:
                    result[date][item["source_type"]] = {}
                result[date][item["source_type"]]["organic"] = visit.get("organic")
                result[date][item["source_type"]]["paid"] = visit.get("paid")

        # print(result)
        date_dict = {}
        for date in result:
            date_dict[date] = {}

        # Loop through the results and add them to the appropriate date dictionary
        for date, data in result.items():
            date_dict[date].update(data)
            date_dict[date].update(output)

        return date_dict
    except Exception as e:
        (
            previous_month_end_date,
            previous_12_month_start_dates,
        ) = calculate_previous_month_dates()
        date_list = []
        for start_date in previous_12_month_start_dates:
            date_list.append(start_date)
        # Check if the current date is after the 10th of the month
        from datetime import datetime

        current_date = datetime.now()
        if current_date.day > 10:
            date_list.append(previous_month_end_date)
            modified_list = [date + "-01" for date in date_list]
            logging.info(
                f"If current date is more than 10th then months list: {modified_list}"
            )
        else:
            modified_list = [date + "-01" for date in date_list]
            logging.info(
                f"If current date is less than 10th then months list: {modified_list}"
            )
        overall_dict = {}
        for date in modified_list:
            date_dict = {date: {"date": date}}
            overall_dict.update(date_dict)
        return overall_dict


count = 0


def dataframe_generator_traffic(site, domain, result_dict, date):
    try:
        # Creating Dataframe and extracting required metrics:
        # print(result_dict)
        data = pd.DataFrame(index=[domain])

        # data["Site"] = domain
        # result_dict = demjson.decode(result_dict)
        logging.info(f"Result Dict: {result_dict}")
        i = 0
        # for date, result_dict in result_dict1.items():
        try:
            try:
                data["Site"] = site
            except:
                data["Site"] = 0

            try:
                data["date"] = date
            except:
                data["date"] = 0
            try:
                data["GlobalRank"] = result_dict["global_rank"]
            except:
                data["GlobalRank"] = 0
            try:
                data["CountryRank"] = result_dict["country_rank"]
            except:
                data["CountryRank"] = 0
            try:
                data["LeadCountry"] = result_dict["lead_country"]
            except:
                data["LeadCountry"] = "No Data"
            try:
                data["Category"] = result_dict["category"]
            except:
                data["Category"] = "No Data"
            try:
                data["CategoryRank"] = result_dict["category_rank"]
            except:
                data["CategoryRank"] = 0

            try:
                data["MonthlyTraffic"] = result_dict["monthly_traffic"]
            except:
                data["MonthlyTraffic"] = 0
            try:
                data["Avg_TimeOnSite"] = result_dict["average_visit_duration"]
            except:
                data["Avg_TimeOnSite"] = 0
            try:
                data["Avg_PageViews"] = result_dict["pages_per_visit"]
            except:
                data["Avg_PageViews"] = 0
            try:
                data["BounceRate"] = result_dict["bounce_rate"]
            except:
                data["BounceRate"] = 0.0
            try:
                data["TopCountry_1"] = result_dict["top_country1"]
            except:
                data["TopCountry_1"] = "No Data"
            try:
                data["TopCountryTraffic_1"] = int(
                    float(result_dict["top_country1_pct"])
                )
            except:
                data["TopCountryTraffic_1"] = 0.0
            try:
                data["TopCountry_2"] = result_dict["top_country2"]
            except:
                data["TopCountry_2"] = "No Data"
            try:
                data["TopCountryTraffic_2"] = int(
                    float(result_dict["top_country2_pct"])
                )
            except:
                data["TopCountryTraffic_2"] = 0.0
            try:
                data["TopCountry_3"] = result_dict["top_country3"]
            except:
                data["TopCountry_3"] = "No Data"
            try:
                data["TopCountryTraffic_3"] = int(
                    float(result_dict["top_country3_pct"])
                )
            except:
                data["TopCountryTraffic_3"] = 0.0
            try:
                data["TopCountry_4"] = result_dict["top_country4"]
            except:
                data["TopCountry_4"] = "No Data"
            try:
                data["TopCountryTraffic_4"] = int(
                    float(result_dict["top_country4_pct"])
                )
            except:
                data["TopCountryTraffic_4"] = 0.0
            try:
                data["TopCountry_5"] = result_dict["top_country5"]
            except:
                data["TopCountry_5"] = "No Data"
            try:
                data["TopCountryTraffic_5"] = int(
                    float(result_dict["top_country5_pct"])
                )
            except:
                data["TopCountryTraffic_5"] = 0.0
            try:
                data["DirectTraffic_organic"] = int(
                    float(result_dict["Direct"]["organic"])
                )
            except:
                data["DirectTraffic_organic"] = 0
            try:
                data["DirectTraffic_pct"] = result_dict["Direct"]["paid"]
            except:
                data["DirectTraffic_pct"] = 0.0
            try:
                data["Search_organic"] = int(float(result_dict["Search"]["organic"]))
            except:
                data["Search_organic"] = 0
            try:
                data["Search_pct"] = result_dict["Search"]["paid"]
            except:
                data["Search_pct"] = 0.0
            try:
                data["DisplayAds_organic"] = int(
                    float(result_dict["Display Ads"]["organic"])
                )
            except:
                data["DisplayAds_organic"] = 0
            try:
                data["DisplayAds_pct"] = result_dict["Display Ads"]["paid"]
            except:
                data["DisplayAds_pct"] = 0.0
            try:
                data["ReferredTraffic_organic"] = int(
                    float(result_dict["Referrals"]["organic"])
                )
            except:
                data["ReferredTraffic_organic"] = 0
            try:
                data["ReferredTraffic_pct"] = result_dict["Referrals"]["paid"]
            except:
                data["ReferredTraffic_pct"] = 0.0
            try:
                data["SocialTraffic_organic"] = int(
                    float(result_dict["Social"]["organic"])
                )
            except:
                data["SocialTraffic_organic"] = 0
            try:
                data["SocialTraffic_pct"] = result_dict["Social"]["paid"]
            except:
                data["SocialTraffic_pct"] = 0.0
            try:
                data["MailTraffic_organic"] = int(float(result_dict["Mail"]["organic"]))
            except:
                data["MailTraffic_organic"] = 0
            try:
                data["MailTraffic_pct"] = result_dict["Mail"]["paid"]
            except:
                data["MailTraffic_pct"] = 0.0

            data["SearchTraffic"] = data["Search_organic"] + data["Search_pct"]
            data["DirectTraffic"] = (
                data["DirectTraffic_organic"] + data["DirectTraffic_pct"]
            )
            data["ReferredTraffic"] = (
                data["ReferredTraffic_organic"] + data["ReferredTraffic_pct"]
            )
            data["MailTraffic"] = data["MailTraffic_organic"] + data["MailTraffic_pct"]
            data["SocialTraffic"] = (
                data["SocialTraffic_organic"] + data["SocialTraffic_pct"]
            )

            # add SearchTraffic in the future
            data["OrganicTraffic"] = (
                data["DirectTraffic_organic"]
                + data["ReferredTraffic_organic"]
                + data["MailTraffic_organic"]
                + data["SocialTraffic_organic"]
                + data["DisplayAds_organic"]
            )
            data["PaidTraffic"] = (
                data["DirectTraffic_pct"]
                + data["ReferredTraffic_pct"]
                + data["MailTraffic_pct"]
                + data["SocialTraffic_pct"]
                + data["DisplayAds_pct"]
            )

            # try:
            #     data["Social_1"] = result_dict["traffic"]["sources"]["social"]["top_socials"][
            #         0
            #     ]["site"]
            # except:
            #     data["Social_1"] = "NoSocial"
            # try:
            #     data["Social_1_traffic"] = result_dict["traffic"]["sources"]["social"][
            #         "top_socials"
            #     ][0]["value"]
            # except:
            #     data["Social_1_traffic"] = 0
            # try:
            #     data["Social_1_traffic_pct"] = (
            #         result_dict["traffic"]["sources"]["social"]["top_socials"][0]["percent"]
            #         / 100
            #     )
            # except:
            #     data["Social_1_traffic_pct"] = 0.0
            # try:
            #     data["Social_2"] = result_dict["traffic"]["sources"]["social"]["top_socials"][
            #         1
            #     ]["site"]
            # except:
            #     data["Social_2"] = "NoSocial"
            # try:
            #     data["Social_2_traffic"] = result_dict["traffic"]["sources"]["social"][
            #         "top_socials"
            #     ][1]["value"]
            # except:
            #     data["Social_2_traffic"] = 0
            # try:
            #     data["Social_2_traffic_pct"] = (
            #         result_dict["traffic"]["sources"]["social"]["top_socials"][1]["percent"]
            #         / 100
            #     )
            # except:
            #     data["Social_2_traffic_pct"] = 0.0
            # try:
            #     data["Social_3"] = result_dict["traffic"]["sources"]["social"]["top_socials"][
            #         2
            #     ]["site"]
            # except:
            #     data["Social_3"] = "NoSocial"
            # try:
            #     data["Social_3_traffic"] = result_dict["traffic"]["sources"]["social"][
            #         "top_socials"
            #     ][2]["value"]
            # except:
            #     data["Social_3_traffic"] = 0
            # try:
            #     data["Social_3_traffic_pct"] = (
            #         result_dict["traffic"]["sources"]["social"]["top_socials"][2]["percent"]
            #         / 100
            #     )
            # except:
            #     data["Social_3_traffic_pct"] = 0.0

            logging.info(f"{domain} dataframe generated")
            logging.info(f"Data : {data}")
            return data
        except Exception as e:
            logging.error(f"DFS Df Generator Traffic Function: {e}")
    except Exception as e:
        logging.error(f"DFS Df Generator Traffic Function: {e}")


# def similar_site_extract(site, domain, result_dict):
#     try:
#         # Extracting similar sites and appending to similar_sites.csv file:
#         competitors = []
#         similar_sites = pd.DataFrame(columns=[site])
#         try:
#             for i in range(len(result_dict["sites"]["similar_sites"])):
#                 competitors.append(result_dict["sites"]["similar_sites"][i]["site"])
#             similar_sites[site] = competitors
#             print(f"Competitors for {domain} extracted")
#         except:
#             competitors = ["Not Found"] * 10
#             similar_sites[site] = competitors
#             print(f"Competitors for {domain} not found")
#         return similar_sites
#     except Exception as e:
#         logging.error(f"DFS Similar Site Extract Function: {e}")


def domain_extractor(site_list):
    try:
        # Extracting domains as requested by DataforSEO from site list:
        domains_dict = {}
        for url in site_list:
            ext = tldextract.extract(url)
            extract_url = ext.domain + "." + ext.suffix
            domains_dict[url] = extract_url
        return domains_dict
    except Exception as e:
        logging.error(f"DFS Domain Extractor Function: {e}")


# Data preprocessing
def data_preprocessing(df):
    try:
        # convert 'Avg_TimeOnSite' from string to numeric value
        df["Avg_TimeOnSite"] = df["Avg_TimeOnSite"].fillna("00:00:00")
        df["Avg_TimeOnSite"] = df["Avg_TimeOnSite"].replace("0", "00:00:00")
        df["Avg_TimeOnSite"] = pd.to_datetime(df["Avg_TimeOnSite"])
        df["Avg_TimeOnSite"] = (
            df["Avg_TimeOnSite"].dt.second
            + df["Avg_TimeOnSite"].dt.minute * 60
            + df["Avg_TimeOnSite"].dt.hour * 3600
        )
        # df['Avg_TimeOnSite'] = df['Avg_TimeOnSite'].fillna(0)
        string_cols = df.select_dtypes(exclude=np.number).columns.tolist()
        # Replacing nulls with mean
        for col in string_cols:
            if df[col].str.contains("error").any():
                df[col] = df[col].replace("error", np.nan)
                # df[col] = df[col].apply(lambda x: np.nan if 'error' else x)
                df[col] = pd.to_numeric(df[col], errors="coerce")
                # df[col].replace(np.nan, df[col].mean(), inplace=True)
                df[col] = df[col].astype(float)

        numeric = df.select_dtypes(include=np.number).columns.tolist()
        df = df.replace(0, np.nan)
        return df
    except Exception as e:
        logging.error(f"DFS Data Preprocessing Function: {e}")


# convert prediction of 'Avg_TimeOnSite' from numeric data to time format
def convert_time(arr):
    try:
        time_arr = []
        for n in arr:
            # time_arr.append(pd.to_timedelta(n, unit='s'))
            hours = n // 3600
            minutes = (n - hours * 3600) // 60
            seconds = n - hours * 3600 - minutes * 60
            time_arr.append("%02d:%02d:%02d" % (hours, minutes, seconds))
        return time_arr
    except Exception as e:
        logging.error(f"DFS Convert Time Function: {e}")


def dataforseo(data_dict, login_dict):
    client = RestClient(login_dict["username"], login_dict["key"])
    site_list = data_dict["site_list"]
    folder_date = data_dict["timestamp"]
    domains_dict = domain_extractor(site_list)
    # Calling API for all sites in list:

    from concurrent.futures import ThreadPoolExecutor, as_completed

    processes = []
    processes_backlinks = []
    final_dataset = pd.DataFrame()
    with ThreadPoolExecutor(max_workers=1) as executor:
        for site, domain in domains_dict.items():
            try:
                result_dict_traffic = []
                result_dict_backlinks = []
                processes.append(executor.submit(rapid_api_metrics, domain))
                processes_backlinks.append(
                    executor.submit(check_status_code, domain, client)
                )

                for task in as_completed(processes):
                    result_dict_traffic = task.result()
                    # print(f"Results: {result_dict_traffic}")
                for task in as_completed(processes_backlinks):
                    result_dict_backlinks = task.result()

                backlinks_data = dataframe_generator_backlinks(
                    site, domain, result_dict_backlinks
                )
                try:
                    for date, i in result_dict_traffic.items():
                        traffic_data = dataframe_generator_traffic(
                            site, domain, i, date
                        )
                        traffic_backlinks = pd.merge(traffic_data, backlinks_data)
                        final_dataset = pd.concat([final_dataset, traffic_backlinks])
                        final_dataset.drop(
                            final_dataset.columns[
                                final_dataset.columns.str.contains(
                                    "unnamed", case=False
                                )
                            ],
                            axis=1,
                            inplace=True,
                            errors="ignore",
                        )
                except Exception as e:
                    logging.error(f"Final Dataframes Creators Error: {e}")

            except Exception as e:
                logging.error(f"Error in Multithreading Process of DFS: {e}")
        cols_list = list(final_dataset.columns)
        function_name = "dataforseo"
        # if "Site" in cols_list:
        #     cols_list.remove("Site")
        for date, df in final_dataset.groupby(by=["date"]):
            path = "{0}/{1}_{2}_{0}.csv".format(
                date, function_name, data_dict["container_name"]
            )
            azs = AzureStorage(data_dict["container_name"])
            azs.upload_blob_dfs(df[cols_list], path, folder_date)

    return final_dataset
