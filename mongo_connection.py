# python -m pip install "pymongo[srv]"==3.11
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv(override=True)

def connect():
    try:
        client = MongoClient(f"mongodb+srv://joulupukki:{os.getenv('PASSWORD')}@cluster0.37ex2rd.mongodb.net/?retryWrites=true&w=majority")
        print("connected to mongo")
        return client
    except:
        print("connection error")

def fetch_new_id(coll):
    id = coll.find_one(sort=[('id',-1)])  
    if id is not None:  
        return int(id['id'])+1   
    else:
        return 0

def fetch_task_by_id(coll,task_id):
    task = coll.find_one({"id":task_id})
    return task