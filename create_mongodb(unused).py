from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000")  # Remember your uri string

col = client['tweets1']['covid']


if __name__ == "__main__":
    
    col.create_index("id", unique=True)
