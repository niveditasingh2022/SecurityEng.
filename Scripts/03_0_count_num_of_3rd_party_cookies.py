import os
import pandas as pd
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument('--dir', help='Directory path for the CSV files')
args = parser.parse_args()

if args.dir:
    directory = args.dir
else:
    directory = input("Please enter the directory path for scanning CSV files: ")

output_data = [['File', 'Total Cookies', '3rd Party Cookies']]

for filename in os.listdir(directory):
    if filename.endswith("_3rd_party.csv"):
        df = pd.read_csv(os.path.join(directory, filename))
        # Total number of cookies
        total_cookies = df.shape[0]
        # Number of third party cookies
        third_party_cookies = df['3rd_party'].value_counts().get(True, 0)
        output_data.append([filename.replace('_3rd_party.csv', ''), total_cookies, third_party_cookies])

with open('num_of_3rd_party_cookies.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output_data)
