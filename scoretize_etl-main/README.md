# Scoretize ETL

This repository contains an Azure Function App that performs ETL (Extract, Transform, Load) operations for Scoretize. The functions are designed to be called by Azure Data Factory pipelines. The purpose of this ETL is to extract data from various sources, calculate a score representing a company's digital marketing performance relative to its competitors, and store the extracted data and score in an Azure SQL Database for display on Scoretize.



## Functions Overview

There are three types of main functions in this repository:

1. **Extract Functions**: Extract digital marketing information from APIs or by web scraping.
2. **Load Functions**: Load the extracted data into the Azure SQL Database.
3. **Score Functions**: Retrieve the digital marketing data from the Azure SQL Database, calculate a score based on the data, and store the score in the database.



## Pipelines Overview

The functions are called by pipelines of Azure Data Factory. These pipelines coordinate the functions and communicate with the backend of the Scoretize application.

Using the Data Factory pipeline the backend executes the "Control" pipeline, sending a configuration dictionary as an argument.


## Control

The backend calls the "Control" pipeline which calls in turn the "Extract-Load" pipeline. Once said pipeline finishes, "Control" calls the "Score-Load" pipeline. After both pipelines have been sucesfully finished, "Control" calls a function to communicate to the backend that both pipelines have been executed sucesfully. In turn if the pipelines fail, a function will be triggered to communicate that the pipeline has failed.

Control passes the configuration dictionary that it has received from the backend to the functions and pipelines it calls.


## Extract-Load pipeline

This pipeline calls the extract functions in the correct order.

Each of this function stores the data it extracts in Azure Storage as an intermediate step, in a container definied by the dictionary the Scoretize backend sends to the pipeline (which are in turn passed to each of the functions called by the pipeline). The container name is definied in the dictionary in the key:value "container_name", and the folder will be the timestamp sent by the dictionary.

Once all of the extract functions are done, the pipeline will call the "Load" functions. 

Each Load function has a particular domain (facebook, web data, social data, etc) and uploads ONLY to one table.

These functions download the csv files from Azure Storage, check and clean the data to make sure to conform to the Schema of the Azure SQL table each data will be uploaded to, and then uploads the data in the table.


## Score-Load pipeline

This pipeline calls the Score functions in the correct order.

Each Score function has a particular domain (facebook, web data, social data, etc).

Each of this function downloads the relevant data from the SQL database (some functions will download data from different tables), performs the neccesary calculations to get a score, and stores this score in Azure Storage.

Once the Score function of each domain is executed, the "final score" function will be executed, and will retrieve all the scores from Azure Storage.

When we finally have the final score the Load functions will upload all the scores to its corresponding tables.


## Visual representation

CONTROL PIPELINE
![image](https://user-images.githubusercontent.com/57181418/227964814-bb61384c-70c9-4c4e-be51-23b80ea9f6ed.png)

EXTRACT-LOAD PIPELINE
![image](https://user-images.githubusercontent.com/57181418/227965598-a5d643d7-9c8d-4b8a-9534-a6a5a0e447e3.png)

SCORE-LOAD PIPELINE
![image](https://user-images.githubusercontent.com/57181418/227966008-117b304f-2ff5-43b5-a2d9-0314e4a9dc31.png)



  ----------------------
  
  ### Input (test) to Http-function
  ```javascript
 {
        "client_id": 670,
        "project_id": 477,
        "sector_id": 45,
        "site_list": [
            "https://credit-suisse.com",
            "https://morganstanley.com",
            "https://citi.com",
            "https://wellsfargo.com"
        ],
        "new_site_list": [
            "https://credit-suisse.com",
            "https://morganstanley.com",
            "https://citi.com",
            "https://wellsfargo.com"
        ],
        "company_id": [
            670,
            671,
            672,
            673
        ],
        "new_company_id": [
            670,
            671,
            672,
            673
        ],
        "container_name": "tkf-477",
        "timestamp": "2023-03-28",
        "unique_ids": {
            "https://credit-suisse.com": 670458863,
            "https://morganstanley.com": 671807838,
            "https://citi.com": 672166401,
            "https://wellsfargo.com": 673547335
        },
        "new_unique_ids": {
            "https://credit-suisse.com": 670458863,
            "https://morganstanley.com": 671807838,
            "https://citi.com": 672166401,
            "https://wellsfargo.com": 673547335
        }
}
```


  --------------------------
  
  
  
  
  # API's
  ### __SOCIAL__
  
    `Social WebScraper` = Returns the company's url for each of the following social medias.
  
    `Facebook` = Facebook WebScraper 
  
    `Instagram` = Instagram WebScraper 
  
    `Twitter` = Twitter WebScraper
  
    `Youtube` = Youtube WebScraper
  
    `Sharedcount` = Search for posts where the company was mentioned
  
  ### __WEB__
  
    `Pagespeed` = Website performance
  
  ### __SEO__
    
    `DataforSEO` = 
    
    `Spyfu` = 
  




  
