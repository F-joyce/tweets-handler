from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://127.0.0.1:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000")  # Remember your uri string

col = client['tweets1']['covid']

# col.create_index("id", unique=True)

df = pd.read_pickle("./df_norm.pkl")

data = df.to_dict(orient='records')  # Here's our added param..

def main():
    for tweet in data:
        try:
            col.insert_one(tweet)
        except:
            continue

if __name__ == "__main__":
    main()