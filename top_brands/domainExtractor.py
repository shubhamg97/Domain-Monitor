# import categoryExtractor
import tldextract
import webapi

# def get_domain_names(inputFile, limit, outputFile, date):
def get_domain_names(inputFile, limit, date):
    # Create dictionary of trademarks
    brand = dict()
    # Counter to keep track of dataset limit
    counter1 = 0
    # Counter to track how many original domains
    counter2 = 0

    # Write the headers on top of the outputFile.txt
    # oFile = open(outputFile, 'w')
    # oFile.write("Rank")
    # oFile.write('\t')
    # oFile.write("Brand")
    # oFile.write('\t')
    # oFile.write("Domain")
    # oFile.write('\t')
    # oFile.write("Category")
    # oFile.write('\n')

    with open(inputFile, 'r') as f:
        for line in f:
            # Increment counter1
            counter1 += 1

            # If counter1 exceeds limit: exit function
            if counter1 > limit:
                # oFile.close()
                break

            # Split the line information to get the rank and full domain name
            rank, fulldomain = line.strip().split('\t')

            # Get the 2LD information from the full domain name
            domain = tldextract.extract(fulldomain)

            # If domain doesn't exist in the dictionary
            if domain.domain not in brand:
                # Increment original domain name counter
                counter2 += 1

                # Add to dictionary and an output file with rank, domain and full domain name information
                brand[domain.domain] = rank

                # Print information on console
                print(rank),
                print('\t'),
                print(domain.domain),
                print('\t'),
                print(fulldomain),
                print('\n')

                # Calls the web_api function to query the PDNS database
                tmpVar = webapi.web_api(domain.domain, fulldomain, date)

                # Calls cateogry_extractor inside categoryExtractor to find the category of a domain
                # category = categoryExtractor.category_extractor(fulldomain)

                # Populate the ouputFile.txt with the values
                # oFile.write(rank)
                # oFile.write('\t')
                # oFile.write(domain.domain)
                # oFile.write('\t')
                # oFile.write(fulldomain)
                # oFile.write('\t')
                # oFile.write(category)
                # oFile.write('\n')

    # Print information
    print("--- --- --- --- ---")
    print("Number of original domains: ")
    print(counter2)

    # Close the output file
    # oFile.close()
