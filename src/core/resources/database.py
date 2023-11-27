import os

from dotenv import load_dotenv
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient

load_dotenv()

uri = os.getenv("MONGO_DB_URI", "")

client = MongoClient(uri)

db = PyMongo()
