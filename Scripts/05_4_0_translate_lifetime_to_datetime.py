import sys
import pandas as pd
import os
import glob
from datetime import timedelta, datetime

def convert_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    months, days = divmod(days, 30)
    years, months = divmod(months, 12)
    
    result = []
    if years:
        result.append(f"{years} years")
    if months:
        result.append(f"{months} months")
    if days:
        result.append(f"{days} days")
    if hours:
        result.append(f"{hours} hours")
    if minutes:
        result.append(f"{minutes} minutes")
    if seconds:
        result.append(f"{seconds} seconds")
    return ', '.join(result)

## Input argument check and define the directory
if len(sys.argv) < 2:
    directory = input("Please enter the directory path for scanning *_3rd_party.csv: ")
else:
    directory = sys.argv[1]

# Get a list of all relevant files
files = glob.glob(os.path.join(directory, '*_3rd_party.csv'))

# Loop through each file
for file in files:
    # Load the CSV data into a dataframe
    data = pd.read_csv(file)

    # Convert the 'Lifetime' column to datetime format and store in a new column
    #data['Lifetime (datetime)'] = pd.to_datetime(data['Lifetime'], unit='s')
    # Convert the 'Lifetime' column to timedelta and convert it into a human readable format
    data['Lifetime (datetime)'] = data['Lifetime'].apply(convert_seconds)

    # Add a new column 'Over 1 year' 
    data['Over 1 year'] = data['Lifetime'].apply(lambda x: True if x > 365*24*60*60 else False)

    # Extract required columns
    data = data[['Page', 'Lifetime', 'Lifetime (datetime)', 'Over 1 year', 'expires', '3rd_party', 'page_domain', 'cookie_domain']]
    #data.style.applymap(color_red, subset=['Over 1 year']).to_excel(new_file_name, engine='openpyxl', index=False)

    # Write the data to a new CSV file
    new_file_name = file.replace('_3rd_party.csv', '_lifecycle_datetime.csv')
    data.to_csv(new_file_name, index=False)
