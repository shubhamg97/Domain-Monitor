import phase2
import utils
import os
import sys
from tldextract import extract

def phishtank_checker(domain_name):
    # If the domain matches one of the phishtank records:
    if db.phishtank.find({"fqdn": domain_name}).count() > 0:
        # Try: update the collection record that phishtank was detected
        try:
            db[collectionName].update_one({"domain": domain_name}, {"$push": {"detected_phishtank": "yes"}})
            print ("Phishtank records found and inserted to database")
        # If unable to update: print error message
        except:
            print ("Phishtank records found but unable to insert to database")
    # Otherwise:
    else:
        # Try: update the collection record that phishtank wasn't detected
        try:
            db[collectionName].update_one({"domain": domain_name}, {"$push": {"detected_phishtank": "no"}})
            print ("No phishtank records found but inserted to database")
        # If unable to update: print error message
        except:
            print ("Phishtank records not found and unable to insert to database")

def virustotal_checker(domain_name):
    # Pass in domain and April 1st 2018 as parameters. The date is included so that only results from April 1st 2018 are checked
    parameters = (domain_name, '2018-04-01')
    query = "SELECT first_detected, last_detected, mal_count, sus_count FROM vt WHERE domain = ? and last_detected >= ?"
    # Perform the query with the given parameters
    c.execute(query, parameters)
    results =  c.fetchone()

    try:
        # If virustotal has records for a given domain:
        if len(results) > 2: # >2 because 1 length is given each for first_detected & last_detected
            # Try: update the collection record that virustotal was detected
            try:
                db[collectionName].update_one({"domain": domain_name}, {"$push": {"detected_virustotal": "yes", "first_detected": results[0], "last_detected": results[1], "mal_count": results[2], "sus_count": results[3]}})
                print ("Virustotal records found and inserted to database")
            # If unable to update: print error message
            except:
                print ("Virustotal records found but unable to insert to database")

    except:
        # Try: update the collection record that virustotal wasn't detected
        try:
            db[collectionName].update_one({"domain": domain_name}, {"$push": {"detected_virustotal": "no"}})
            print ("No virustotal records found but inserted to database")
        # If unable to update: print error message
        except:
            print ("Virustotal records not found and unable to insert to database")

def central_dnstwist(inputFile, limit):
    # Create a limit counter
    counter = 0
    # Open the file to read it
    with open(inputFile, 'r') as f:
        # For each line of domain
        for line in f:
            # Isolate and get the domain name
            rank, domain = line.strip().split('\t')
            # Get the 2LD domain name from the domain
            rawDomain = extract(domain)

            # If raw domain is one of the domains from the search engine list: pass
            if rawDomain.domain in searchEngines:
                pass

            # Else: add all of the domains to the collection and perform the below function
            else:
                # Increment counter and if counter exceeds limit: break
                counter += 1
                if counter > limit:
                    break

                twistedDomains = utils.get_dnstwist(domain)

                try:
                    # If domain is already in the collection: do nothing
                    if db[collectionName].find({"domain": domain}).count() > 0:
                        pass
                    else:
                        # Else: insert the twisted domains into the collection
                        db[collectionName].insert({"domain": domain, "dnstwist": twistedDomains})
                except:
                    # If twistedDomains is None
                    print ("This domain has no DNSTWIST information")

                # Add phishtank and virustotal records
                phishtank_checker(domain)
                virustotal_checker(domain)

                # Pass the domain name into phase2
                phase2.register_domain(domain)
                phase2.twisted_domain(domain)

                # Conclude function for the given domain
                print ("DNSTWIST INFORMATION FOR " + domain + " IS NOW IN DATABASE IN COLLECTION: " + collectionName)

##--------------MAIN Program--------------------

# Exclusions list of the most popular search engines
searchEngines = ["google", "bing", "baidu", "yahoo", "ask", "aol", "wolframalpha", "duckduckgo", "yandex"]

# Establish connection with sqlite3
c = utils.connect_sqlite()

# Establish connection with MongoDB
db = utils.connect_mongo()

# Get the timestamp for when data is queried
timestamp = utils.get_timestamp()
collectionName = "dnstwist_" + timestamp

# Input format for running program manually
# inputFile = raw_input('Enter the file source: ')
# limit = int(input('Enter the datapush limit: '))
# Input format for running through crontab
inputFile = sys.argv[1]
limit = int(sys.argv[2])

# Call the function
central_dnstwist(inputFile, limit)
