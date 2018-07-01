import psycopg2
from pymongo import MongoClient

def connect_mongo():
    # Establish connection with MongoDB
    client = MongoClient("mongodb://squatting:squatting123@10.2.4.231/squatting_db")
    return client.squatting_db

def connect_postgres():
    return psycopg2.connect(database = "phishing", user = "postgres", password = "postgres", port = 5432)
