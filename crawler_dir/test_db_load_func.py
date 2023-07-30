from pymongo import MongoClient

def load_db(data):
    client = MongoClient("mongodb://localhost:27017/")
    db = client.get_database()





















