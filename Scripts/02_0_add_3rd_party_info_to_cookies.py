import csv
import argparse
import os
import tldextract

# Set argument parsing
parser = argparse.ArgumentParser(description='Extract 3rd party cookies from a CSV file.')
parser.add_argument('file', nargs='?', type=str, help='The CSV file to process.')
args = parser.parse_args()

# Request file name input if the user has not provided one
if args.file is None:
    args.file = input("Please enter the file name to extract 3rd party info: ")

# Declar a list for storing results
result_data = []

# Open CSV file
with open(args.file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    # Extract header information
    headers = reader.fieldnames
    if headers is not None:
        for col_name in ['3rd_party', 'page_domain', 'cookie_domain']:
            if col_name not in headers:
                headers.append(col_name)    
    
    # Process each row
    for row in reader:
        page_domain = tldextract.extract(row.get("Page")).domain
        #page_domain = row.get("Page").split('.')[0]
        cookie_domain = tldextract.extract(row.get("domain").lstrip(".")).domain

        row['page_domain'] = page_domain
        row['cookie_domain'] = cookie_domain

        # Compare page domain and cookie domain
        if page_domain and cookie_domain and page_domain not in cookie_domain:
            row['3rd_party'] = "True"
        else:
            row['3rd_party'] = "False"

        result_data.append(row)

# Save the results into a CSV file
output_filename = os.path.splitext(args.file)[0] + "_3rd_party.csv"

with open(output_filename, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    for data in result_data:
        writer.writerow(data)
