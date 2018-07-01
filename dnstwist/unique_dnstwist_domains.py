import os
import sys
import utils

# Input format for running program manually
# inputFile = raw_input('Enter the file source: ')
# limit = int(input('Enter the dataset limit: '))
# Input format for running through crontab
inputFile = sys.argv[1]
limit = int(sys.argv[2])

# Establish connection with MongoDB
db = utils.connect_mongo()
# Get the timestamp for when data is queried
timestamp = utils.get_timestamp()
# Set a limit counter
counter = 0

# Open the file to read it
with open(inputFile, 'r') as f:
    # For each line of domain
    for line in f:
        # Increment counter and if counter exceeds limit: break
        counter += 1
        if counter > limit:
            break

        # Isolate and get the domain name
        rank, domain = line.strip().split('\t')

        twistedDomains = utils.get_dnstwist(domain)

        try:
            # For the content in the JSON file
            for item in twistedDomains:
                # If domain is already in collection: update the lastSeen date
                if db.dnstwist_unique_domains.find({"domain": domain}).count() > 0:
                    db.dnstwist_unique_domains.update_one({"domain": domain}, {"$set": {"last_seen": timestamp}})
                    print ("DNSTWIST INFORMATION FOR \"" + domain + "\" HAS BEEN UPDATED INTO THE DATABASE")
                # Otherwise, insert the record into the collection
                else:
                    db.dnstwist_unique_domains.insert({"domain": domain, "first_seen": timestamp, "last_seen": timestamp, "dnstwist": item})
                    print ("DNSTWIST INFORMATION FOR \"" + domain + "\" HAS BEEN INSERTED INTO THE DATABASE")
        except:
            # If twistedDomains returns None
            print ("No DNSTWIST information exists for " + domain)
