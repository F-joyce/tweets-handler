import requests
import json
import os
from itertools import zip_longest
from dotenv import load_dotenv
from pymongo import MongoClient
import time
import datetime

load_dotenv()

bearer_token = os.getenv('T_btoken') 


client = MongoClient('localhost:27017')
col_to = client['tweets']['updated']
col_to.create_index("id", unique=True)
col_from = client['tweets']['trial']

# print(col_from)

def grouper(iterable, n, fillvalue=None): # Groups long list in chunks of 99 manageable by Twitter API
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

# for x in grouper([1,2,3,4,5,6,7,8,9,10], 2):
#     print(list(x))

def create_list_ids():
    list_ids = []
    for tweet in col_from.find():
        list_ids.append(tweet['data']['id'])
    return list_ids

# print(create_list_ids())

def create_url(list_100_id, fields = 'public_metrics'):
    list_ids = ','.join(list_100_id) if len(list_100_id)>1 else list_100_id[0]
    ids = f"ids={list_ids}"
    fields = f"tweet.fields={fields}"

    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, fields)
    # print(url)
    return url

# urls = create_url(['a','b','c'])

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["Content-Type"] = "application/json"
    return r

aapi = 0

def connect_to_api(url):

    response = requests.get(url, auth=bearer_oauth)
    
    print(response.status_code)

    if response.status_code != 200:
        raise Exception(
            "Something did not work {} : {}".format(
                response.status_code, response.text
            )
        )

    # print(response.json())
    
    return response

# connect_to_api(urls)

def main():

    lista = create_list_ids()

    to_add = []

    for chunk in grouper(lista, 100):
        try:
            url = create_url(list(chunk))
            response = connect_to_api(url)
            to_add.append(response.json())
            remaining_req = int(response.headers['x-rate-limit-remaining'])
            if  remaining_req < 295:
                col_to.insert_many(to_add)
                print(f'Only {remaining_req} requests remaining')
                seconds_left = int(response.headers['x-rate-limit-reset']) - int(time.time())
                print(f'Waiting {seconds_left} seconds for the rate limit window to reset')
                time.sleep(seconds_left)
        except TypeError:
            set_ids = list(set(list(chunk)))

            set_ids.remove(None)
            
            url = create_url(list(set_ids))

            to_add_to = connect_to_api(url)

            to_add.append(to_add_to.json())

    col_to.insert_many(to_add)

main()