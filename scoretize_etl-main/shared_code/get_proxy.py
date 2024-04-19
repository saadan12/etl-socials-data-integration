import urllib.request
import random
from shared_code.storage_functions import AzureStorage
import time 
import logging

def get_proxy():
    path = 'brightdata.json'
    az = AzureStorage("config-files")
    config_dict = az.download_blob_dict(path)
    username = config_dict['username']
    password = config_dict['password']
    port = config_dict['port']
    start_time = time.time()
    session_id = random.random()
    super_proxy_url = ('http://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' %
        (username, session_id, password, port))
    proxy_handler = urllib.request.ProxyHandler({
        'http': super_proxy_url,
        'https': super_proxy_url,
    })
    opener = urllib.request.build_opener(proxy_handler)
    print('Performing request')
    print(opener.open('http://lumtest.com/myip.json').read())
    if time.time() - start_time > 5:
        logging.info('proxy time out, requesting again....')
        get_proxy()
    print('this is proxy', super_proxy_url)
    return super_proxy_url
