from urlparse import urlparse
import utils

# Try and connect to the MongoDB database
try:
    db = utils.connect_mongo()
    print("Connected to MongoDB")
# If exception caught, print that connection failed and exit
except:
    print("Unable to connect to MongoDB")
    exit(1)

# Try and connect to the PostgreSQL database
try:
    connection = utils.connect_postgres()
    print("Connected to PostgreSQL")
# If exception caught, print that connection failed and exit
except:
    print("Unable to connect to PostgreSQL")
    exit(1)

# Point to the cursor of the connection
cursor = connection.cursor()
# In the cursor, load the url from the phishtank database
cursor.execute("SELECT url from phishtank")
# Inside the variable 'rows', get all the url's
rows = cursor.fetchall()

# For all the items in 'rows', parse and get their FQDN
for items in rows:
    parsedDomain = urlparse(items[0])
    fqdn = '{url.netloc}'.format(url = parsedDomain)

    # If the domain is in the collection: move on
    if db.phishtank.find({"fqdn": fqdn}).count() > 0:
        print("Domain is already in the collection")
        pass
    # Otherwise, add it
    else:
        db.phishtank.insert({"fqdn": fqdn})
        print("Domain " + fqdn + " inserted to MongoDB successfully")

# Print success and completion of function message
print("\nAll domains from PostgreSQL 'phishtank' database successfully stored in MongoDB under 'phishtank' collection")
