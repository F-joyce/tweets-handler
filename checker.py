from pymongo import MongoClient
import pandas as pd
import pprint

client = MongoClient("mongodb://127.0.0.1:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000")  # Remember your uri string

db = client['tweets1']

col = db['covid']

_ = 0

for tweet in col.find(): 
    print(str(_) + '\n' + tweet['tweet'] + '\n') 
    _ += 1