import logging
from shared_code.storage_functions import AzureStorage, df_to_sql_companywise
from shared_code.database_helpers import clean_pre_db
from shared_code.db_schemas import CompanyWiseScores_TblSchema
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    input_config = req.get_json()
    azs = AzureStorage(input_config["container_name"])
    score_table(azs, input_config)

    return func.HttpResponse("Table loaded")


def score_table(azs: AzureStorage, data_dict: dict):
    date_list = []
    date_dfs = azs.download_blob_dfs_date(
        data_dict["container_name"], data_dict["timestamp"]
    )
    date_list = [blob.split("/")[0] for blob in date_dfs]
    # Get the latest date
    date = max(date_list)
    for i in date_list:
        if i == date:
            logging.info(date)
            final_path = "{0}/scores/{1}_{2}_{0}.csv".format(
                data_dict["timestamp"], "final_score", data_dict["container_name"]
            )
            score_df = azs.download_blob_df(final_path)
            logging.info(f"Final score: {score_df}")

            social_path = "{0}/subscores/{1}_{2}_{0}.csv".format(
                data_dict["timestamp"], "social", data_dict["container_name"]
            )
            social_df = azs.download_blob_df(social_path)
            logging.info(f"Social subscore: {social_df}")

            logging.info(f"Social subscore: {social_df}")
            score_df["initial_date"] = i

            db_df = score_df[["initial_date"]]
            db_df["Site"] = score_df["Site"]
            db_df["global_score"] = score_df["score_total"]
            db_df["website_score"] = score_df["score_website"]
            db_df["sm_score"] = score_df["score_social"]
            db_df["sm_facebook_score"] = social_df["fb_score"]
            db_df["sm_instagram_score"] = social_df["insta_score"]
            db_df["sm_youtube_score"] = social_df["youtube_score"]
            db_df["sm_twitter_score"] = social_df["twitter_score"]
            db_df["seo_score"] = score_df["score_seo"]
            db_df["project_id"] = data_dict["project_id"]
            db_df["searchAds_score"] = score_df["score_searchads"]

            companies_id = [data_dict["unique_ids"][site] for site in db_df["Site"]]

            logging.info(f"Companies proceded: {db_df['Site']}")
            logging.info(f"Company ids: {companies_id}")

            db_df = db_df.drop("Site", axis=1)

            db_df["company_id"] = companies_id

            score = CompanyWiseScores_TblSchema()
            db_df = clean_pre_db(db_df, score)
            logging.info(f"Clean df: {db_df.to_string()}")
            df_to_sql_companywise(i, db_df, "api_company_wise_scores", dtype=score)
        else:
            logging.info(f"PRINT DATE: {i}")
            score = "website"
            final_path = "{0}/subscores/website/{1}_{2}_{3}.csv".format(
                data_dict["timestamp"], score, data_dict["container_name"], i
            )
            score_df = azs.download_blob_df(final_path)
            logging.info(f"Final score: {score_df}")

            score_df["initial_date"] = i

            db_df = score_df[["initial_date"]]
            db_df["Site"] = score_df["Site"]
            db_df["global_score"] = score_df["score_website"]
            db_df["website_score"] = score_df["score_website"]
            db_df["sm_score"] = 0
            db_df["sm_facebook_score"] = 0
            db_df["sm_instagram_score"] = 0
            db_df["sm_youtube_score"] = 0
            db_df["sm_twitter_score"] = 0
            db_df["seo_score"] = 0
            db_df["project_id"] = data_dict["project_id"]
            db_df["searchAds_score"] = 0
            companies_id = [data_dict["unique_ids"][site] for site in db_df["Site"]]

            logging.info(f"Companies proceded: {db_df['Site']}")
            logging.info(f"Company ids: {companies_id}")

            db_df = db_df.drop("Site", axis=1)

            db_df["company_id"] = companies_id
            logging.info(f"Load Company score df :{db_df}")

            score = CompanyWiseScores_TblSchema()
            db_df = clean_pre_db(db_df, score)
            logging.info(f"Clean df: {db_df.to_string()}")
            df_to_sql_companywise(i, db_df, "api_company_wise_scores", dtype=score)
