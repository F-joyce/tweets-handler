import requests
import requests.auth
import pandas as pd
import json
import os

R_client_id = os.getenv('R_client_id') 
R_client_secret = os.getenv('R_client_secret') 
R_username = os.getenv('R_username')
R_password = os.getenv('R_password')
R_user_agent = os.getenv('R_user_agent') 


LIMIT = str(50)

def dump_in(namefile, data):
    with open(namefile, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_token():
        auth = requests.auth.HTTPBasicAuth(R_client_id, R_client_secret)

        data = {'grant_type': 'password',
                'username': R_username,
                'password': R_password}

        headers = {"User-Agent":R_user_agent}

        res = requests.post('https://www.reddit.com/api/v1/access_token',
        auth=auth, data=data, headers=headers)

        # print(res.json()) Uncomment if bad requests to check token is fetched

        token = res.json()['access_token']

        return token


if 'TOKEN' in globals():
        print('Token already fetched')
else:
        TOKEN = get_token()
        print(f"New token is {TOKEN}")

headers = {"Authorization":f"bearer {TOKEN}",
                "User-Agent":R_user_agent}

headers_limit = headers.copy()
headers_limit['limit'] = LIMIT

response_submissions = requests.get('https://oauth.reddit.com/r/all/hot', headers=headers_limit)

listing_submissions = response_submissions.json()['data']['children']

list_link = []

# Gets the top 25 hot submissions in r/all and note the link_id
for submission in listing_submissions:
        list_link.append(submission['data']['name'].replace('t3_',''))

print(list_link)


dict_comments = {}

# Use the link_id to get the comment tree of the 25 hot submission, put the body of the comments in a list
for link_id in list_link:
        list_comments = []
        comment_tree_full = requests.get(f'https://oauth.reddit.com/r/all/comments/{link_id}', headers=headers_limit)
        
        # dump_in('dove.json', comment_tree_full.json())
        
        comment_tree = comment_tree_full.json()

        for list in comment_tree:
                for comment in list['data']['children']: 
                        try:
                                list_comments.append(comment['data']['body'])
                        except KeyError:
                                continue
                        
        dict_comments[link_id] = list_comments
        
df = pd.DataFrame.from_dict(dict_comments, orient='index')



df.transpose().to_pickle('./comment_trees.pkl')