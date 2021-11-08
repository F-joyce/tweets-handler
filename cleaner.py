from pymongo import MongoClient
import datetime

client = MongoClient("mongodb://127.0.0.1:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000")  # Remember your uri string

col = client['tweets1']['covid']

# TODO 
# substitute date with DATE parameter shared

date = (datetime.datetime.utcnow() - datetime.timedelta(hours = 24)).strftime('%Y-%m-%d %H:%M:%S')

query_to_clear = { "date" : { "$lt" : date }}


# to_clear = col.find(query_to_clear)

# for x in to_clear:
#     col.delete_one(x)

if __name__ == "__main__":
    
    col.delete_many(query_to_clear)