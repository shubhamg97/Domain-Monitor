from pymongo import MongoClient
import os
import pymongo
import utils

def register_domain(domain_name):
    db = utils.connect_mongo()
    # If domain is registered_domain collection: pass
    if db.registered_domain.find({"domain": domain_name}).count() > 0:
        pass
    # Else: insert the domain in the collection and the date when it was added
    else:
        db.registered_domain.insert({"domain": domain_name, "date": utils.get_timestamp()})

def twisted_domain(domain_name):
    db = utils.connect_mongo()
    # Get twisted domains
    twistedDomains = utils.get_dnstwist(domain_name)
    # Collection name for domain name
    collectionName = "domain_" + domain_name

    if twistedDomains == None:
        pass

    else:
        for domain in twistedDomains:
            try:
                if db[collectionName].find({"domain-name": domain["domain-name"]}).count() > 0:
                    # Update last seen date
                    db[collectionName].update_one({"domain-name": domain["domain-name"]}, {"$set": {"date_last_seen": utils.get_timestamp()}})
                else:
                    # Insert to database
                    db[collectionName].insert({"date_first_seen": utils.get_timestamp(), "date_last_seen": utils.get_timestamp(), "twisted": domain})
            except Exception:
                print("Exception caught in phase2.py --> twisted_domain")
                pass
