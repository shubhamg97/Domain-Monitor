from pymongo import MongoClient

# Get mongodb database client connection object
def connect_mongo():
  client = MongoClient("mongodb://squatting:squatting123@localhost/squatting_db")
  return client.squatting_db

