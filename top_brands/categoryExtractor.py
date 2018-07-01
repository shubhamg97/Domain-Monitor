from bs4 import BeautifulSoup
import re
import requests

def category_extractor(domain):
    # The prefix used for the full domain name
    fortiguard = "https://fortiguard.com/webfilter?q="
    # The domain that is passed in
    alexadomain = domain
    # Concatenate the two strings together
    url = fortiguard + alexadomain
    # Create header information for the request that is sent
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    # Gets a response to a request for the url and headers passed in
    response = requests.get(url, headers = headers)

    # Creates an instance of BeautifulSoup and parses the HTML response content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Finds the category
    category = soup.find("h4", attrs = {"class": "info_title"})
    
    # Converts category to string and if not found, then returns default output
    try:
        category = category.text.strip()
        # Removes "Category: " from the string
        category = re.sub(r'^\W*\w+\W*', '', category)
    except:
        category = "Not Found"

    # Return the category
    return category
