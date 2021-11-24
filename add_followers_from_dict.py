import pandas as pd
import json

with open('temp_usernames.json') as json_file:
    lista = json.load(json_file)

user_followers = {}

for n in range(len(lista['data'])):
    user_followers[lista['data'][n]['username']] = lista['data'][n]['public_metrics']['followers_count']
    
df = pd.read_pickle('./df_clean.pkl')

df['nFollowers'] = df['username'].map(user_followers)

df.to_pickle('./df_followers.pkl')

