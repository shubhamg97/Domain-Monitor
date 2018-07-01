from urllib2 import HTTPError
import json
import pprint
import pymongo
import time
import urllib2

client = pymongo.MongoClient("mongodb://squatting:squatting123@10.2.4.231/squatting_db") # defaults to port 27017
db = client.squatting_db

def query_params(first_before, first_after, last_before, last_after):
    # Make initial query_str empty
    query_str = ""
    # If there is a first_before value: convert to epoch time and add to query_str
    if (first_before != None):
        epoch_first_before = str(time.mktime(time.strptime(first_before, '%Y%m%d %H:%M')))
        if len(query_str) > 0:
            query_str += "&"
        query_str += "time_first_before="
        query_str += epoch_first_before

    # If there is a first_after value: convert to epoch time and add to query_str
    if (first_after != None):
        epoch_first_after = str(time.mktime(time.strptime(first_after, '%Y%m%d %H:%M')))
        if len(query_str) > 0:
          query_str += "&"
        query_str += "time_first_after="
        query_str += epoch_first_after

    # If there is a last_before value: convert to epoch time and add to query_str
    if (last_before != None):
        epoch_last_before = str(time.mktime(time.strptime(last_before, '%Y%m%d %H:%M')))
        if len(query_str) > 0:
          query_str += "&"
        query_str += "time_last_before="
        query_str += epoch_last_before

    # If there is a last_after value: convert to epoch time and add to query_str
    if (last_after != None):
        epoch_last_after = str(time.mktime(time.strptime(last_after, '%Y%m%d %H:%M')))
        if len(query_str) > 0:
          query_str += "&"
        query_str += "time_last_after="
        query_str += epoch_last_after

    # Return the final query_str with a limit of 100 results
    # return (query_str + "&limit=100")

    # Return the final query_str
    return (query_str)


def dns_query(domain, first_before, first_after, last_before, last_after):
    # Create a query string from the function above to pass into the WebAPI
    query = query_params(first_before, first_after, last_before, last_after)
    # If there is a query, append a '?' in the front
    if len(query) > 0:
        query = "?" + query

    # Create a string of the URL to query
    domainFormat = "http://10.2.4.218/lookup/rrset/name/{}/A{}".format(domain, query)
    # Create a request with specific header values
    request = urllib2.Request(domainFormat,
        headers = {
            'Accept': 'application/json',
            'X-API-Key': '82827cf79576078112b80646585a583b081edcaba91bf6f7898c6ee1725febf7'
    })

    # Try and query the PDNSDB with the WebAPI, if exception caught, if it's a 404/504 error, return NULL, else: throw the error
    try:
        response = urllib2.urlopen(request)
        ipObjects = [json.loads(obj) for obj in response]
        return ipObjects
    except HTTPError as e:
        if e.code == 404:
            return None
        if e.code == 504:
            return None
        else:
            raise


def get_unique_name(jsonList):
    unique_rrname = set()

    try:
        for obj in jsonList:
            unique_rrname.add(obj["rrname"])
            return list(unique_rrname)
    except:
        return None


def web_api(brand, domain, date):
    # Create different types of wildcard brands for the PDNS query searches
    wildcard1 = "*." + brand + ".*"
    wildcard2 = "*." + brand
    # wildcard3 = brand + ".*"

    # Create a collection with the name = combosquatting_date
    collectionName = 'combosquatting_' + date

    # Append times to the date for the search parameters
    beginningTime = str(date) + " 00:00"
    endingTime = str(date) + " 23:59"

    # Create a list for the lastSeen and firstSeen lists
    lastSeenList1 = dns_query(wildcard1, None, None, endingTime, beginningTime)
    lastSeenList2 = dns_query(wildcard2, None, None, endingTime, beginningTime)
    # lastSeenList3 = dns_query(wildcard3, None, None, endingTime, beginningTime)
    firstSeenList1 = dns_query(wildcard1, endingTime, beginningTime, None, None)
    firstSeenList2 = dns_query(wildcard2, endingTime, beginningTime, None, None)
    # firstSeenList3 = dns_query(wildcard3, endingTime, beginningTime, None, None)

    # Get the unique domains for each list
    lastSeenDomains1 = get_unique_name(lastSeenList1)
    lastSeenDomains2 = get_unique_name(lastSeenList2)
    # lastSeenDomains3 = get_unique_name(lastSeenList3)
    firstSeenDomains1 = get_unique_name(firstSeenList1)
    firstSeenDomains2 = get_unique_name(firstSeenList2)
    # firstSeenDomains3 = get_unique_name(firstSeenList3)

    # Pass the brand, the domain, and the 2 unique domain lists from the query into the collection: combosquatting_YYYYMMDD
    db[collectionName].insert({"brand": brand, "domain": domain, "last_seen_unique_domains": lastSeenDomains1, "first_seen_unique_domains": firstSeenDomains1})
    db[collectionName].update_one({"brand": brand}, {"$push": {"last_seen_unique_domains": lastSeenDomains2, "first_seen_unique_domains": firstSeenDomains2}})
    # db[collectionName].update_one({"brand": brand}, {"$push": {"last_seen_unique_domains": lastSeenDomains3, "first_seen_unique_domains": firstSeenDomains3}})
