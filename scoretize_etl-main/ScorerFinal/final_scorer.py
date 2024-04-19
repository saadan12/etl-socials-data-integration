from shared_code.storage_functions import AzureStorage
import pandas as pd
import logging
import pandas as pd
import numpy as np
from shared_code import functions_score_transform as f


def score_function(df):
    # Totalcols = ["Site", "score_reputation", "score_seo", "score_social", "score_website", 
    #      "score_searchads"]

    # since we don't have repuation
    Totalcols = ["Site", "score_seo", "score_social", "score_website", "score_searchads"]     
    #Keeping only score columns that are included in dataset
    df = f.column_adjuster(df, Totalcols)   
    #Weights of each column
    # weights= {"score_reputation" : 0.10, "score_seo" : 0.2, "score_social" : 0.10, "score_website" : 0.3, "score_searchads" : 0.3}
    weights= {"score_seo" : 0.30, "score_social" : 0.30, "score_website" : 0.4, "score_searchads" : 0.1}

    #Redistributing weights if features are missing
    weights= f.redistribute_weights(df, weights)
    #Applying score
    df_final=df.copy()
    #Applying score
    df= f.create_bestSite(df, Totalcols[1:])
    df = f.apply_score(df, weights, "score_total", 50, 100)
    df=df[(df["Site"]!="BestSite") & (df["Site"]!="WorstSite")]
    df_final["score_total"]=df["score_total"]
    df_final = df_final.dropna(axis=1, how='all')
    
    return df_final


def final_scorer(data_dict):
    try:
        container_name = data_dict["container_name"]
        timestamp = data_dict["timestamp"]
        #Establishing connection to Azure Storage
        azs = AzureStorage(container_name)
        # scores= ["reputation", "seo", "social", "website", "searchads"]
        scores= ["seo", "social", "website", "searchads"]
        
        df_list= []
        #LatesT Date getting from DFS Folders
        date_dfs = azs.download_blob_dfs_date(data_dict["container_name"],data_dict["timestamp"])
        date_list = [blob.split("/")[0] for blob in date_dfs]
        # Get the latest date
        date = max(date_list)
        #Downloading sub-scores and combining into one dataframe
        for score in scores: 
            if score == "website":
                path = "{0}/subscores/website/{1}_{2}_{3}.csv".format(timestamp, score, container_name,date)
            else:
                path = "{0}/subscores/{1}_{2}_{0}.csv".format(timestamp, score, container_name)
            df= azs.download_blob_df(path)
            score_column_name= "score_" + score
            df= df[["Site", score_column_name]]
            df_list.append(df)
            dfs = [df.set_index('Site') for df in df_list]
            df=pd.concat(dfs, axis=1)
            df=df.reset_index()
            df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True, errors="ignore")
        #Applying final score to dataset
        df = score_function(df)
        #Defining final score path
        score_path = "{0}/scores/final_score_{1}_{0}.csv".format(timestamp, container_name)
        #Uploading final score to blob
        azs.upload_blob_df(df, score_path)

        return "ok"

    except Exception as e:
        logging.exception(e)
        return "ok"