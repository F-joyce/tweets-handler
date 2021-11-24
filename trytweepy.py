import requests
import json
import ENV_VAR
import pandas as pd
from itertools import zip_longest

bearer_token = ENV_VAR.B_TOKEN

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

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

users_list = []

df = pd.read_pickle("./df_clean.pkl")

for user in df['username']:
    if user not in users_list:
        users_list.append(user)

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


with open('temp_usernames.json', 'w') as outfile:
    json.dump(json_response, outfile)

# url = create_url(users_list[:98], user_fields)

# json_response = connect_to_endpoint(url)

# with open('temp_usernames.json', 'w') as outfile:
#     json.dump(json_response, outfile)



# print(json.dumps(json_response, indent=4, sort_keys=True))

# dict ={}

# for n in range(len(json_response['data'])):
#     dict[json_response['data'][n]['username']] = json_response['data'][n]["public_metrics"]["followers_count"]
