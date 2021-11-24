import pandas as pd
from pandas.io import pickle

usernames_list = []

df = pd.read_pickle("./df_clean.pkl")

for user in df['username']:
    if user not in usernames_list:
        usernames_list.append(user)
        
