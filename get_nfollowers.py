import requests
import json
import pandas as pd
from itertools import zip_longest
import os
from dotenv import load_dotenv

load_dotenv()

'''Connects to the twitter API and gets the n_followers for each username of the tweets fetched, as
    this needs to be done at a later time than when tweets are collected'''



bearer_token = os.getenv('T_btoken')

def grouper(iterable, n, fillvalue=None): # Groups long list in chunks of 99 manageable by Twitter API
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def create_list_usernames(): # Create a list of usernames from the fetched dataframe
    users_list = []

    df = pd.read_pickle("./df_clean.pkl")

    for user in df['username']:
        if user not in users_list:
            users_list.append(user)
    return users_list

def create_url(user_names_list, user_fields):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    user_names = ','.join(user_names_list) if len(user_names_list)>1 else user_names_list[0]
    
    usernames = f"usernames={user_names}"
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    print(url)
    return url

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r

def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def main():
    users_list = create_list_usernames()

    user_fields = "user.fields=public_metrics"

    json_response = {'data': []}

    for chunk_users in grouper(users_list, 99):
        try:
            url = create_url(list(chunk_users), user_fields)

            to_add = connect_to_endpoint(url)

            json_response['data'].extend(to_add['data'])

        except TypeError:
            set_users = list(set(list(chunk_users)))

            set_users.remove(None)
            
            url = create_url(list(set_users), user_fields)

            to_add = connect_to_endpoint(url)

            json_response['data'].extend(to_add['data'])


    with open('temp_usernames_trial.json', 'w') as outfile:
        json.dump(json_response, outfile)

if __name__ == "__main__":
    main()