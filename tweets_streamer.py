import requests
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv() # Load the .env file with secret tokens etc

LIMIT = 50000 

BATCH = 100

client = MongoClient("mongodb://127.0.0.1:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000")  # Remember your uri string

col = client['tweets']['trial'] # This is the database collection name, change 'tweets' and 'trial' with what you'd like

bearer_token = os.getenv('T_btoken') 

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["Content-Type"] = "application/json"
    return r


def set_rules(check_syntax = True):

    rules = [{"value": "@covid OR covid19 OR covid-19 OR coronavirus OR pfizer OR astrazeneca OR omicron -is:retweet", "tag": "no retweets"}]
    payload = {"add": rules}

    response = requests.post("https://api.twitter.com/2/tweets/search/stream/rules?dry_run={}".format(check_syntax), auth=bearer_oauth, json=payload)
    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))

def get_rules():

    response = requests.get("https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

    print("This is GETTING existing rules:" + json.dumps(response.json()))

    return response.json()

def delete_all_rules():
    rules = get_rules()
    try:
        rules_ids = [x["id"] for x in rules['data']]
    except KeyError:
        
        return print('No existing rules') 
    print('Updated rules are', rules_ids)
    
    payload = {"delete": {'ids' : rules_ids}}

    response = requests.post("https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth, json=payload)
    
    print(response.status_code, response.text)

def get_stream(sample=True):
    if sample == True:
        sample = 'sample'
    else:
        sample = 'search'

    fields = "lang,public_metrics,referenced_tweets"
    user_fields = "public_metrics"

    response = requests.get("https://api.twitter.com/2/tweets/{}/stream?tweet.fields={}&expansions=author_id&user.fields={}".format(sample,fields,user_fields) , auth=bearer_oauth, stream=True)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )

    counter = 0

    counter_tweets = 0

    list_filtered = []
    
    for response_line in response.iter_lines():
        if counter_tweets < LIMIT:
            if counter%1000 ==0:
                print("Iteration number {}".format(counter))
            counter += 1
            if response_line:
                json_response = json.loads(response_line)
                
                try:

                    if json_response['data']['lang'] == 'en':

                        if 'referenced_tweets' not in json_response['data']:
                            counter_tweets += 1
                            list_filtered.append(json_response)
                            if counter_tweets%100 == 0:
                                print('Appending {} tweet to MONGO, total is {}'.format(len(list_filtered),counter_tweets))
                                col.insert_many(list_filtered)
                                list_filtered = []
                except:
                    continue        
        else:
            print(f"Fetched {counter_tweets} tweets, filtered from a total of {counter}, saved on mongodb tweets.trial")
            break

    print("Out of loop")


def main():
    get_stream()

if __name__ == "__main__":
    main()