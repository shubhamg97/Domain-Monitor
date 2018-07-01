from datetime import datetime
from pymongo import MongoClient
import json
import os
import sqlite3

def connect_mongo():
    # Establish connection with MongoDB
    client = MongoClient("mongodb://squatting:squatting123@10.2.4.231/squatting_db")
    return client.squatting_db

def connect_sqlite():
    # Establish connection with SQLite3
    conn = sqlite3.connect('/export/sec02/moi/vt2.db')
    return conn.cursor()

def get_dnstwist(domain):
    # Perform the dnstwist search for a domain and store it in a JSON file
    os.system("python ~/dnstwist/dnstwist.py --json " + domain + " > dnstwist.json")

    # Load the information from the JSON file
    page = open("dnstwist.json", 'r')
    parsed = None
    try:
        parsed = json.loads(page.read())
    except:
        print("No dnstwist records for this domain")
        pass
    os.remove("dnstwist.json")
    return parsed

def get_timestamp():
    # Return current date in format YYYYMMDD
    return str(datetime.now().strftime("%Y%m%d"))
