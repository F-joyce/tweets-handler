from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://127.0.0.1:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000")  # Remember your uri string

col = client['tweets1']['covid']


for doc in col.model.find({'tweet'}): 
    print(doc) 