from datetime import datetime
import domainExtractor
# import jsonCreator

inputFile = raw_input('Enter the file source: ')
limit = int(input("Enter the dataset limit: "))
date = str(input("Enter the date for PDNS query: "))
date = datetime.strptime(date, '%Y%m%d').strftime("%Y%m%d")
# outputFile = 'outputFile.txt'

domainExtractor.get_domain_names(inputFile, limit, date)
# domainExtractor.get_domain_names(inputFile, limit, outputFile, date)
# jsonCreator.txt_to_json(limit, outputFile)

print("PROGRAM EXECUTION COMPLETED")
