import sqlalchemy as sa
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.core.exceptions import HttpResponseError, ResourceExistsError
import io
import pandas as pd
import json
from urllib import parse
import logging
from shared_code.settings import AZURE_STORAGE, SERVER, DATABASE, USERNAME, PASSWORD


####################################################################
#                            AZURE STORAGE
####################################################################


class AzureStorage:
    def __init__(self, container_name: str):
        self.connect_str = AZURE_STORAGE
        logging.info(
            f"Connecting to Azure Storage with connection string {self.connect_str}"
        )
        # Create the BlobServiceClient object which will be used to create a container client
        self.blob_service_client = BlobServiceClient.from_connection_string(
            self.connect_str
        )
        self.container_name = container_name
        logging.info(f"Connected to Azure Storage to container name {container_name}")

    def upload_blob_df(self, df: pd.DataFrame, path: str):
        logging.info(f"Uploading blob to {path}", extra={"dataframe.info": df.info()})
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=path
            )
            output = io.StringIO()
            output = df.to_csv(encoding="utf-8")
            blob_client.upload_blob(
                output, blob_type="BlockBlob", tags={"overwrite": "True"}
            )
            logging.info(f"Successfully uploaded blob to {path}")
        except ResourceExistsError:
            logging.info(
                f"Blob already exists in {path}", extra={"dataframe.info": df.info()}
            )
            pass

    def upload_blob_dfs(self, df: pd.DataFrame, path: str, date: str):
        logging.info(f"Uploading blob to {path}", extra={"dataframe.info": df.info()})
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name, blob=f"{date}/dataforseo/{path}"
            )
            output = io.StringIO()
            output = df.to_csv(encoding="utf-8")
            blob_client.upload_blob(
                output, blob_type="BlockBlob", tags={"overwrite": "True"}
            )
            logging.info(f"Successfully uploaded blob to {path}")
        except ResourceExistsError:
            logging.info(
                f"Blob already exists in {path}", extra={"dataframe.info": df.info()}
            )
            pass

    def download_blob_df(self, path):
        logging.info(f"Downloading blob from {path}")
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name, blob=path
        )
        downloaded_blob = blob_client.download_blob()
        df = pd.read_csv(io.StringIO(downloaded_blob.content_as_text()))
        logging.info(
            "Successfully downloaded blob",
            extra={"path": path, "dataframe.info": df.info()},
        )
        return df

    def download_blob_dfs_date(self, container_name, date):
        container_client = self.blob_service_client.get_container_client(
            container=self.container_name
        )
        blobs = container_client.list_blobs(name_starts_with=f"{date}/dataforseo/")
        folder_names = set()
        lis1 = []
        for blob in blobs:
            relative_path = blob.name.replace(f"{date}/dataforseo/", "")
            lis1.append(relative_path)

        return lis1

    def download_blob_dfs(self, path, date):
        logging.info(f"Downloading blob from {path}")
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name, blob=f"{date}/dataforseo/{path}"
        )
        downloaded_blob = blob_client.download_blob()
        df = pd.read_csv(io.StringIO(downloaded_blob.content_as_text()))
        logging.info(
            "Successfully downloaded blob",
            extra={"path": path, "dataframe.info": df.info()},
        )
        return df

    def download_blob_folder(self, folder_path):
        logging.info(f"Downloading blob from {folder_path}")
        container_client = self.blob_service_client.get_container_client(
            container=self.container_name
        )
        files_path = []
        for file in container_client.walk_blobs(folder_path):
            files_path.append(file.name)
        logging.info("Successfully downloaded folder", extra={"path": folder_path})
        return files_path

    def download_blob_dict(self, path):
        logging.info(f"Downloading blob from {path}")
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name, blob=path
        )
        downloaded_blob = blob_client.download_blob()
        dict_blob = json.loads(downloaded_blob.readall())
        logging.info(
            "Successfully downloaded blob", extra={"path": path, "output": dict_blob}
        )
        return dict_blob

    def blob_exists(self, blob_path) -> bool:
        blob = BlobClient.from_connection_string(
            conn_str=self.connect_str,
            container_name=self.container_name,
            blob_name=blob_path,
        )
        return blob.exists()

    def delete_blob(self, blob_path):
        blob_client = BlobClient.from_connection_string(
            conn_str=self.connect_str,
            container_name=self.container_name,
            blob_name=blob_path,
        )

        blob_client.delete_blob()
        logging.info("Successfully deleted blob", extra={"path": blob_path})

    def container_exists(self):
        container_client = self.blob_service_client.get_container_client(
            container=self.container_name
        )
        return container_client.exists()

    def create_container(self):
        logging.info(f"Trying to create container named {self.container_name}")
        container_client = self.blob_service_client.get_container_client(
            container=self.container_name
        )
        container_client.create_container()
        logging.info(f"Successfully created container {self.container_name}")


####################################################################
#                            AZURE DATABASE
####################################################################


def df_to_sql(df: pd.DataFrame, table, dtype, identity_value=False):
    string = (
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + SERVER
        + ";DATABASE="
        + DATABASE
        + ";UID="
        + USERNAME
        + ";PWD="
        + PASSWORD
    )

    params = parse.quote_plus(string)

    logging.info(f"Params: {params}")

    engine = sa.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

    if identity_value:
        with engine.begin() as conn:
            conn.exec_driver_sql(f"SET IDENTITY_INSERT [{DATABASE}].[dbo].{table} ON")
            df.to_sql(
                table,
                schema="dbo",
                con=conn,
                index=False,
                if_exists="append",
                dtype=dtype.sqlalchemy_dtypes,
            )
            conn.exec_driver_sql(f"SET IDENTITY_INSERT [{DATABASE}].[dbo].{table} OFF")
    else:
        df.to_sql(
            table,
            schema="dbo",
            con=engine,
            index=False,
            if_exists="append",
            dtype=dtype.sqlalchemy_dtypes,
        )


import numpy as np


def df_to_sql_website(df: pd.DataFrame, table, dtype, identity_value=False):
    string = (
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + SERVER
        + ";DATABASE="
        + DATABASE
        + ";UID="
        + USERNAME
        + ";PWD="
        + PASSWORD
    )

    params = parse.quote_plus(string)

    logging.info(f"Params: {params}")

    engine = sa.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

    with engine.begin() as conn:
        for index, row in df.iterrows():
            # Check if the ID already exists in the table
            query = (
                f"SELECT COUNT(*) FROM {table} WHERE website_id = '{row['website_id']}'"
            )
            result = conn.execute(query)
            count = result.scalar()

            if count > 0:
                logging.info(f"ID {row['website_id']} already exists in the {table} table.")
                # Perform further actions or return a specific value
            else:
                # ID doesn't exist, insert the data
                if identity_value:
                    conn.exec_driver_sql(
                        f"SET IDENTITY_INSERT [{DATABASE}].[dbo].{table} ON"
                    )
                try:
                    df.loc[[index]].to_sql(
                        table,
                        schema="dbo",
                        con=conn,
                        index=False,
                        if_exists="append",
                        dtype=dtype.sqlalchemy_dtypes,
                    )
                    print(f"Inserted data for ID: {row['website_id']}")
                except Exception as e:
                    print(f"Error inserting data for ID: {row['website_id']}. {str(e)}")
                finally:
                    if identity_value:
                        conn.exec_driver_sql(
                            f"SET IDENTITY_INSERT [{DATABASE}].[dbo].{table} OFF"
                        )


def df_to_sql_website_traffic(df: pd.DataFrame, table, dtype, identity_value=False):
    string = (
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + SERVER
        + ";DATABASE="
        + DATABASE
        + ";UID="
        + USERNAME
        + ";PWD="
        + PASSWORD
    )

    params = parse.quote_plus(string)

    logging.info(f"Params: {params}")

    engine = sa.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

    with engine.begin() as conn:
        for index, row in df.iterrows():
            # Check if the ID already exists in the table
            query = (
                f"SELECT COUNT(*) FROM {table} WHERE website_id = '{row['website_id']}'"
            )
            result = conn.execute(query)
            count = result.scalar()

            if count > 0:
                print(f"ID {row['website_id']} already exists in the {table} table.")
                # Perform further actions or return a specific value
            else:
                # ID doesn't exist, insert the data
                if identity_value:
                    conn.exec_driver_sql(
                        f"SET IDENTITY_INSERT [{DATABASE}].[dbo].{table} ON"
                    )
                try:
                    df.loc[[index]].to_sql(
                        table,
                        schema="dbo",
                        con=conn,
                        index=False,
                        if_exists="append",
                        dtype=dtype.sqlalchemy_dtypes,
                    )
                    print(f"Inserted data for ID: {row['website_id']}")
                except Exception as e:
                    print(f"Error inserting data for ID: {row['website_id']}. {str(e)}")
                finally:
                    if identity_value:
                        conn.exec_driver_sql(
                            f"SET IDENTITY_INSERT [{DATABASE}].[dbo].{table} OFF"
                        )


def df_to_sql_companywise(date, df: pd.DataFrame, table, dtype, identity_value=False):
    string = (
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + SERVER
        + ";DATABASE="
        + DATABASE
        + ";UID="
        + USERNAME
        + ";PWD="
        + PASSWORD
    )

    params = parse.quote_plus(string)

    logging.info(f"Params: {params}")

    engine = sa.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

    with engine.begin() as conn:
        for index, row in df.iterrows():
            # Check if the ID already exists in the table
            query = f"SELECT * FROM api_company_wise_scores WHERE project_id= '{row['project_id']}' and initial_date='{date}';"
            result = conn.execute(query)
            count = result.scalar()

            if count is not None and count > 0:
                print(f"Date {date} already exists in the {table} table.")
                # Perform further actions or return a specific value
            else:
                # ID doesn't exist, insert the data
                if identity_value:
                    conn.exec_driver_sql(
                        f"SET IDENTITY_INSERT [{DATABASE}].[dbo].{table} ON"
                    )
                    df.to_sql(
                        table,
                        schema="dbo",
                        con=conn,
                        index=False,
                        if_exists="append",
                        dtype=dtype.sqlalchemy_dtypes,
                    )
                    conn.exec_driver_sql(
                        f"SET IDENTITY_INSERT [{DATABASE}].[dbo].{table} OFF"
                    )
                else:
                    df.to_sql(
                        table,
                        schema="dbo",
                        con=conn,
                        index=False,
                        if_exists="append",
                        dtype=dtype.sqlalchemy_dtypes,
                    )
                print(f"Inserted data for ID: {date}")


def df_to_sql_social_child(df: pd.DataFrame, table, dtype, identity_value=False):
    string = (
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + SERVER
        + ";DATABASE="
        + DATABASE
        + ";UID="
        + USERNAME
        + ";PWD="
        + PASSWORD
    )

    params = parse.quote_plus(string)

    logging.info(f"Params: {params}")

    engine = sa.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

    with engine.begin() as conn:
        for index, row in df.iterrows():
            # Check if the ID already exists in the table
            query = f"SELECT COUNT(*) FROM {table} WHERE social_media_id = {row['social_media_id']}"
            result = conn.execute(query)
            count = result.scalar()

            if count > 0:
                print(
                    f"ID {row['social_media_id']} already exists in the {table} table."
                )

                # Perform further actions or return a specific value
            else:
                # ID doesn't exist, insert the data
                if identity_value:
                    conn.exec_driver_sql(
                        f"SET IDENTITY_INSERT [{DATABASE}].[dbo].{table} ON"
                    )
                    df.to_sql(
                        table,
                        schema="dbo",
                        con=conn,
                        index=False,
                        if_exists="append",
                        dtype=dtype.sqlalchemy_dtypes,
                    )
                    conn.exec_driver_sql(
                        f"SET IDENTITY_INSERT [{DATABASE}].[dbo].{table} OFF"
                    )
                else:
                    df.to_sql(
                        table,
                        schema="dbo",
                        con=conn,
                        index=False,
                        if_exists="append",
                        dtype=dtype.sqlalchemy_dtypes,
                    )
                    print(f"Inserted data for ID: {row['social_media_id']}")


def df_to_sql_social(df: pd.DataFrame, table, dtype, identity_value=False):
    string = (
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + SERVER
        + ";DATABASE="
        + DATABASE
        + ";UID="
        + USERNAME
        + ";PWD="
        + PASSWORD
    )

    params = parse.quote_plus(string)

    logging.info(f"Params: {params}")

    engine = sa.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

    with engine.begin() as conn:
        for index, row in df.iterrows():
            # Check if the ID already exists in the table
            query = f"SELECT COUNT(*) FROM {table} WHERE social_id = '{row['social_id']}' AND project_id = {row['project_id']}"
            result = conn.execute(query)
            count = result.scalar()

            if count > 0:
                print(f"ID {row['social_id']} already exists in the {table} table.")

                # Perform further actions or return a specific value
            else:
                # ID doesn't exist, insert the data
                if identity_value:
                    conn.exec_driver_sql(
                        f"SET IDENTITY_INSERT [{DATABASE}].[dbo].{table} ON"
                    )
                try:
                    df.loc[[index]].to_sql(
                        table,
                        schema="dbo",
                        con=conn,
                        index=False,
                        if_exists="append",
                        dtype=dtype.sqlalchemy_dtypes,
                    )
                    print(f"Inserted data for ID: {row['social_id']}")
                except Exception as e:
                    print(f"Error inserting data for ID: {row['social_id']}. {str(e)}")
                finally:
                    if identity_value:
                        conn.exec_driver_sql(
                            f"SET IDENTITY_INSERT [{DATABASE}].[dbo].{table} OFF"
                        )


def df_to_sql_seo(df: pd.DataFrame, table, dtype, identity_value=False):
    string = (
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + SERVER
        + ";DATABASE="
        + DATABASE
        + ";UID="
        + USERNAME
        + ";PWD="
        + PASSWORD
    )

    params = parse.quote_plus(string)

    logging.info(f"Params: {params}")

    engine = sa.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

    with engine.begin() as conn:
        for index, row in df.iterrows():
            # Check if the ID already exists in the table
            query = f"SELECT COUNT(*) FROM {table} WHERE seo_id = '{row['seo_id']}'"
            result = conn.execute(query)
            count = result.scalar()

            if count > 0:
                print(f"ID {row['seo_id']} already exists in the {table} table.")

                # Perform further actions or return a specific value
            else:
                # ID doesn't exist, insert the data
                if identity_value:
                    conn.exec_driver_sql(
                        f"SET IDENTITY_INSERT [{DATABASE}].[dbo].{table} ON"
                    )
                try:
                    df.loc[[index]].to_sql(
                        table,
                        schema="dbo",
                        con=conn,
                        index=False,
                        if_exists="append",
                        dtype=dtype.sqlalchemy_dtypes,
                    )
                    print(f"Inserted data for ID: {row['seo_id']}")
                except Exception as e:
                    print(f"Error inserting data for ID: {row['seo_id']}. {str(e)}")
                finally:
                    if identity_value:
                        conn.exec_driver_sql(
                            f"SET IDENTITY_INSERT [{DATABASE}].[dbo].{table} OFF"
                        )


def sql_to_dataframe(sql_query):
    string = (
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + SERVER
        + ";DATABASE="
        + DATABASE
        + ";UID="
        + USERNAME
        + ";PWD="
        + PASSWORD
    )

    params = parse.quote_plus(string)

    engine = sa.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

    df = pd.read_sql(sql_query, engine)

    return df


def update_sql(df: pd.DataFrame, table, join_col):
    string = (
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + SERVER
        + ";DATABASE="
        + DATABASE
        + ";UID="
        + USERNAME
        + ";PWD="
        + PASSWORD
    )

    params = parse.quote_plus(string)

    logging.info(f"Params: {params}")

    engine = sa.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

    with engine.begin() as conn:
        df.to_sql(
            "temp_table",
            con=conn,
            if_exists="replace",
        )

        sql = f"""
            UPDATE {table}
            SET facebook_url = source.facebook_url, instagram_url = source.instagram_url, twitter_url = source.twitter_url, youtube_url = source.youtube_url
            FROM temp_table as source
            WHERE {table}.{join_col} = source.{join_col}
            """

        conn.exec_driver_sql(sql)


def row_to_df(table, id, id_column):
    query = f"""SELECT TOP (1) * FROM {table}
             WHERE {id_column} = {id}"""

    df = sql_to_dataframe(query)

    return df


def db_to_df(data_dict, table, id_column):
    df_list = []

    unique_ids = data_dict["unique_ids"]

    for site, id in unique_ids.items():
        df = row_to_df(table, id, id_column)
        df["Site"] = site
        df_list.append(df)

    df = pd.concat(df_list)

    return df


def db_to_dfs(data_dict, date, table, id_column):
    df_list = []
    print(f"Date: {date}")
    unique_ids = data_dict["unique_ids"]
    for site, id in unique_ids.items():
        df = row_to_df(table, str(id) + date, id_column)
        df["Site"] = site
        df_list.append(df)

    df = pd.concat(df_list)
    print(df)
    return df

def db_to_dfs_social(data_dict, date, table, id_column):
    df_list = []
    logging.info(f"Date: {date}")
    unique_ids = data_dict["unique_ids"]
    for site, id in unique_ids.items():
        df = row_to_df(table, str(id) + date + str(data_dict['project_id']), id_column)
        df["Site"] = site
        df_list.append(df)

    df = pd.concat(df_list)
    logging.info(f"db_to_dfs: {df}")
    return df
