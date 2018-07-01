import csv

def txt_to_json(limit, outputFile):
    jsonfile = file('domains.json', 'w')
    jsonfile.write('[\r\n')

    with open(outputFile, 'r') as oFile:
        # Skip the heading
        next(oFile)
        # Read the rest of the file
        reader = csv.reader(oFile, delimiter='\t')

        # Initiate counter and get the total number of rows excluding the heading
        counter = 0
        numRows = len(list(reader))

        # Return to first line
        oFile.seek(0)
        # Skip the heading
        next(oFile)

        # For all the headers for each domain
        for rank, brand, domain, category in reader:
            # Increment counter
            counter += 1

            # If counter exceeds limit: break
            if counter > limit:
                oFile.close()
                break

            # Otherwise, write the JSON object
            jsonfile.write('\t{\r\n')

            # Categorically, create a string of information
            r = '\t\t\"rank\": ' + rank + ',\r\n'
            b = '\t\t\"brand\": \"' + brand + '\",\r\n'
            d = '\t\t\"domain\": \"' + domain + '\",\r\n'
            c = '\t\t\"category\": \"' + category + '\"\r\n'

            # And write the string into the JSON file
            jsonfile.write(r)
            jsonfile.write(b)
            jsonfile.write(d)
            jsonfile.write(c)

            jsonfile.write('\t}')

            # Write commas for all items except the last one
            if counter < numRows:
                jsonfile.write(',\r\n')

            jsonfile.write('\r\n')

    # Close bracket and close the JSON file
    jsonfile.write(']')
    jsonfile.close()
