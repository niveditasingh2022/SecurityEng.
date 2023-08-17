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

output_data = [['File', 'Total Cookies', 'Strict', 'Lax', 'None', 'Not set', 'Not set w/ non-secure', 'Not set w/ secure']]

for filename in os.listdir(directory):
    if filename.endswith("_3rd_party.csv"):
        #df = pd.read_csv(os.path.join(directory, filename))
        df = pd.read_csv(os.path.join(directory, filename), keep_default_na=False)
        total_cookies = df.shape[0]

        # Counting each case of {sameSite, secure} pair
        strict = sum(df['sameSite'] == 'Strict')
        lax = sum(df['sameSite'] == 'Lax')
        none = sum(df['sameSite'] == 'None')
        missing = sum(df['sameSite'] == '')
        notset_nonsecure = sum((df['sameSite'] == '') & (df['secure'] == False))
        notset_secure = sum((df['sameSite'] == '') & (df['secure'] == True))

        output_data.append([filename.replace('_3rd_party.csv', ''), total_cookies, strict, lax, none, missing, notset_nonsecure, notset_secure])

with open('samesite_attribute.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output_data)
