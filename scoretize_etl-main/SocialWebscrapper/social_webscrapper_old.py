import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import re
from incapsula import IncapSession
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from random import randint
import logging
import tldextract
from requests_html import HTMLSession
session = HTMLSession()
from urllib.parse import unquote
import instaloader

# Remember to set chromedriver.exe on the same directory as this script!

HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
    "application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8,en-US;q=0.7,pt-PT;q=0.6,pt;q=0.5",
    "Dnt": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
    # 'Cookie': Cookies
}

def validate(platform: str, social_links: list, domain: str):
    extraced_urls =[]
    for link in social_links:

        if platform == "facebook":

            regexp = re.compile(
                r"(?:https?:)?\/\/(?:www\.)?(?:facebook|fb)\.com\/(?P<profile>(?![A-z]+\.php)(?!marketplace|gaming|watch|me|messages|help|search|groups)[A-z0-9_\-\.]+)\/?"
            )

        elif platform == "instagram":

            regexp = re.compile(
                r"(?:https?:)?\/\/(?:www\.)?(?:instagram\.com|instagr\.am)\/(?P<username>[A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)"
            )

        elif platform == "twitter":

            regexp = re.compile(
                r"(?:https?:)?\/\/(?:[A-z]+\.)?twitter\.com\/@?(?!home|share|privacy|tos)(?P<username>[A-z0-9_]+)\/?"
            )

        elif platform == "youtube":

            regexp = re.compile(r'(?:https?:)?\/\/(?:[A-z]+\.)?youtube.com\/?(channel|user|c|(?:[A-z0-9_]))\/?(?:[A-z0-9-\_]+)')

        # linkedin
        else:

            regexp = re.compile(
                r"(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/(?:company|school)\/(?P<company_permalink>[A-z0-9-À-ÿ\.]+)\/?"
            )

        social_search = regexp.search(link)
        if social_search:
            try:
                profile_name = str(social_search.group(0))
                if profile_name:
                    if 'instagram' in profile_name:
                        try:
                            ver_url=profile_name
                            logging.info(f"Google Search Url Instagram: {ver_url}")
                            url = "https://instagram-data1.p.rapidapi.com/user/info"
                            username1=re.search(r'https://www.instagram.com/([^/?]+)', ver_url).group(1)
                            headers= {
                                "X-RapidAPI-Host": "instagram-data1.p.rapidapi.com",
                                "X-RapidAPI-Key": "9c33b473demsh0fd262e6ed2a3f0p1ab63cjsn8e3f12e367ad"
                            }
                            querystring = {"username":username1}

                            response = requests.request("GET", url, headers=headers, params=querystring)
                            res12 = response.json()
                            logging.info(f"Verified Url of Rapid API Insta function: {res12.get('external_url')}")
                            extracted_url = res12.get('external_url')
                            extracted_url = get_real_url_from_shortlink(extracted_url)
                            extraced_urls.append(extracted_url)
                            logging.info(f"Insta Extracted Urls: {extraced_urls}")
                            for i in extraced_urls:
                                extract_url = domain_extractor1(domain)
                                if extract_url in i:
                                    # if domain1 == domain_extacted:
                                    link = ver_url                                
                                    return link
                        except Exception as e:
                            logging.error(f"Instagram Validation Error: {e}")
                    if 'youtube' in profile_name:
                        logging.info(f"Google Search Url Youtube: {profile_name}")
                        try:
                            try:
                                url = "https://youtube-channel-details.p.rapidapi.com/"

                                querystring = {"id":profile_name}

                                headers = {
                                    "X-RapidAPI-Key": "9c33b473demsh0fd262e6ed2a3f0p1ab63cjsn8e3f12e367ad",
                                    "X-RapidAPI-Host": "youtube-channel-details.p.rapidapi.com"
                                }

                                response = requests.request("GET", url, headers=headers, params=querystring).json()
                                logging.info(f"Rapid API Youtube API Response: {response}")
                            except Exception as e:
                                logging.error(f"Rapid Api Youtube Error: {e}")
                            try:            
                                extract_url = domain_extractor1(domain)            
                                if extract_url in response.get('canonicalBaseUrl'):
                                    return link
                            except Exception as e:
                                logging.error(f"Extraction Link Youtube Error: {e}")
                           
                        except Exception as e:
                            logging.error(f"Youtube Validation Error: {e}")
                    if 'facebook' in profile_name:
                        try:
                            logging.info(f"Google Search Url Facebook: {profile_name}")
                            url = "https://facebook-company-data.p.rapidapi.com/fbAboutData"
                            payload = {"FBUrls": [profile_name]}
                            headers = {
                                        "content-type": "application/json",
                                        "X-RapidAPI-Host": "facebook-company-data.p.rapidapi.com",
                                        "X-RapidAPI-Key": "9c33b473demsh0fd262e6ed2a3f0p1ab63cjsn8e3f12e367ad"
                                        }
                            response = requests.request("POST", url, json=payload, headers=headers)
                            res = response.json()['results'][0][profile_name]
                            logging.info(f"Verified Search Url Facebook: {res}")
                            try:
                                if res['page_about_fields']['website']:
                                    extract_url = domain_extractor1(domain)
                                    if extract_url in res['page_about_fields']['website']:
                                        return link
                            except Exception as e:
                                logging.error(f"Facebook Validation Error: {e}")
                            try:
                                if res['Website']:
                                    extract_url = domain_extractor1(domain)
                                    if extract_url in res['Website']:
                                        return link
                            except Exception as e:
                                logging.error(f"Facebook Validation Error: {e}")
                        except Exception as e:
                            logging.error(f"Facebook Validation Error: {e}")   
                    if 'twitter' in profile_name:
                        try:
                            headers={
                            "Content-Type":"text",
                            "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAADDpaAEAAAAAOz6x7xTs%2F4LxuZRaf7h9j3GApv4%3DTeXhaV630Gk4GHNLYmSRIevOdmV6likXq5Aj8JRmxfIANM87op"
                            }
                            username = username =re.search(r'https://twitter.com/([^/?]+)', profile_name).group(1)
                            output = requests.get(f"https://api.twitter.com/2/users/by?usernames={username}&user.fields=entities",headers=headers)
                            logging.info(f"Google Search Url Twitter: {output}")
                            if output:
                                entity = json.loads(output.text)
                                logging.info(f"Verified Search Url Twitter: {entity}")
                                for i in entity['data']:
                                    for j in i['entities']['url']['urls']:
                                        extracted_url = get_real_url_from_shortlink(j['expanded_url'])
                                        extraced_urls.append(extracted_url)
                                        logging.info(f"Twitter Extracted Urls: {extraced_urls}")
                                        extract_url = domain_extractor1(domain)
                                        for k in extraced_urls:
                                            if extract_url in k:
                                                return link
                        except Exception as e:
                            logging.error(f"Twitter Validation Error: {e}")
                        
                    else:
                        if domain.lower() in profile_name.lower():
                            logging.info("Found profile name " + str(profile_name) + " the domain name is " + str(domain))
                            return link
                
                        
            except Exception as e:
                logging.info('Social search Validation Function error: ', e)
    


def domain_extractor(url: str):
    ext = tldextract.extract(url)
    domain = ext.domain
    return url
def domain_extractor1(url: str):
    ext = tldextract.extract(url)
    domain = ext.domain
    return domain

def selenium(url):
    # Disable extensions of chromedriver
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initiate driver
    driver = webdriver.Chrome("chromedriver", options=chrome_options)
    driver.get(url)

    # Wait 2 or 3 seconds for page to load correctly
    WebDriverWait(driver, randint(5, 7))

    # Return soup
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.quit()

    return soup

def get_real_url_from_shortlink(url):
    resp = requests.get(url)    
    return resp.url
def incapsula_crack(url):
    # Link to incapsula bypass explanation: https://github.com/ziplokk1/incapsula-cracker-py3
    session = IncapSession()
    session.headers.update(HEADER)
    response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    return soup


def soup_extractor(soup1,i):
    link_dict = {}
    logging.info(f"Soup Url :{i}")
    try:
        for link in soup1:
            if "facebook.com" in link["href"]:
                facebook = link["href"]
                link_dict["facebook"] = facebook
                

            elif "twitter.com" in link["href"]:
                twitter = link["href"]
                link_dict["twitter"] = twitter

            elif "instagram.com" in link["href"]:
                instagram = link["href"]
                link_dict["instagram"] = instagram

            elif "youtube.com" in link["href"]:
                youtube = link["href"]
                link_dict["youtube"] = youtube

            elif "linkedin.com" in link["href"]:
                linkedin = link["href"]
                link_dict["linkedin"] = linkedin
    except Exception as e:
        logging.error(f"Url Extractor Error: {e}")

        try:
            headers = {
                    "content-type": "application/json",
                    "X-RapidAPI-Host": "facebook-company-data.p.rapidapi.com",
                    "X-RapidAPI-Key": "9c33b473demsh0fd262e6ed2a3f0p1ab63cjsn8e3f12e367ad",
            }
            url = "https://facebook-company-data.p.rapidapi.com/getFBUrl"
            payload = {"url": i}
                    
            response = requests.request("POST", url, json=payload, headers=headers)
            res1 = response.json()["Results"]
            facebook = res1.get('Facebook page url')
            if facebook:
                link_dict["facebook"] = facebook
                logging.info(f"Company Url Response: {facebook}")
        except Exception as e:
            logging.error(f"Outisde Loop Company Url Error: {e}")
    return link_dict


def url_extractor(url):
    try:
        logging.info("Scrapping: " + str(url))
        # # Extracts Facebook, Twitter, Instagram, YouTube from Site (if they exist):
        session = requests.Session()
        session.headers.update(HEADER)

        # Try normal scrapping first
        chrome_options1 = Options()
        chrome_options1.add_argument("--no-sandbox")
        chrome_options1.add_argument("--disable-extensions")
        chrome_options1.add_argument("--headless")
        chrome_options1.add_argument("--disable-dev-shm-usage")
        driver2 = webdriver.Chrome("chromedriver", options=chrome_options1)
        driver2.get(url)
        html = session.get(url)
        WebDriverWait(driver2, randint(5, 9))

    # Return soup
        html = driver2.page_source
        soup = BeautifulSoup(html, "html.parser")
        soup1 = soup.find_all("a")
    
        logging.info(f"Soup Results: {soup1}")
        # If the url detects a bot try with incapsula_crack
        if len(soup.findAll("meta", {"name": "ROBOTS"})) > 0:
            logging.info("Antibot measures detected. Trying with incapsula_crack.")
            soup = incapsula_crack(url)
        driver2.quit()

        # Try to get links out of the soup
        
        link_dict = soup_extractor(soup1,url)

        # If no links were found it might be because the website still detects a bot
        # Or because the links are behind javascript, so as a last effort we try with selenium
        if len(link_dict.keys()) == 0:
            logging.info("No links retrieved. Trying with Selenium")
            soup = selenium(url)
            link_dict = soup_extractor(soup,url)

        logging.info("link_dict: " + str(link_dict))
        platforms = ["facebook", "twitter", "instagram", "youtube", "linkedin"]
        links = []
        for platform in platforms:
            if platform not in link_dict.keys():
                logging.info("Trying with google search")
                domain = domain_extractor(url)

                search_url = (
                    "https://www.google.co.uk/search?q=" + domain + "+" + platform
                )
                soup = selenium(search_url)
                search = soup.find_all("div", class_="yuRUbf")
                for h in search:
                    links.append(h.a.get("href"))

                logging.info("Found these links in google search: " + str(links))
                
                correct_link = validate(platform, links, domain)                
                if correct_link:
                    link_dict[platform] = correct_link

        # If no links were found:
        link_dict["Site"] = url
        link_dict["facebook"] = link_dict.get("facebook", "Not Found")
        link_dict["twitter"] = link_dict.get("twitter", "Not Found")
        link_dict["instagram"] = link_dict.get("instagram", "Not Found")
        link_dict["youtube"] = link_dict.get("youtube", "Not Found")
        link_dict["linkedin"] = link_dict.get("linkedin", "Not Found")

        print(f"URL for {url} extracted")
    except Exception as e:
        print(f"{url} NOT accesible")
        print("ERROR:" + str(e))

        logging.exception("problem in url_extractor() " + str(url))

        link_dict = {
            "Site": url,
            "facebook": "Not Found",
            "twitter": "Not Found",
            "instagram": "Not Found",
            "youtube": "Not Found",
            "linkedin": "Not Found",
        }

        pass
    return link_dict


import concurrent.futures

def social_webscrapper(data_dict):
    print("Crawling websites to find social media links ...")

    site_list = data_dict["site_list"]
    dataset = pd.DataFrame(site_list, columns=["Site"])
    dataset.dropna(inplace=True)
    dataset.drop_duplicates(inplace=True)
    
    def extract_urls(row):
        return url_extractor(row["Site"])
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(extract_urls, dataset.to_dict("records")))
        print(f"Results : {results}")
    dataset = pd.DataFrame(results, columns=["Site", "facebook", "twitter", "instagram", "youtube", "linkedin"])
    
    dataset = dataset.set_index("Site")
    
    return dataset
