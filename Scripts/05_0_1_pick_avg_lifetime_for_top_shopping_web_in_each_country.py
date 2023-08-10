import sys
import pandas as pd
import glob
import os

def create_max_lifetime_csv(directory):
    # Get the list of 'Lifetime_by_web_*.csv' files
    file_list = glob.glob(os.path.join(directory, 'avg_lifetime_by_web*.csv'))

    # Filenames to skip
    skip_files = ['avg_lifetime_by_web_for_All Countries.csv', 
                  'avg_lifetime_by_web_for_All Countries_Less Stricter.csv', 
                  'avg_lifetime_by_web_for_All Countries_Stricter Rule.csv']

    # Initialize a list to store DataFrames
    df_list = []

    for file in file_list:
        # Skip the file if its name is in the skip_files list
        if os.path.basename(file) in skip_files:
            continue

        # Read the CSV file
        data = pd.read_csv(file)
        country = os.path.basename(file).split('.csv')[0].split('_')[-1]
        if country in ['France', 'Germany', 'Italy', 'Spain', 'USA', 'Australia', 'Canada', 'India', 'Japan']:
            site = 'amazon'
        elif country == 'Netherlands':
            site = 'bol'
        elif country == 'Poland':
            site = 'olx'
        elif country == 'Sweden':
            site = 'blocket'
        elif country == 'Brazil':
            site = 'mercadolivre'
        elif country == 'Chile':
            site = 'mercadolibre'
        elif country == 'China':
            site = 'lightinthebox'
        elif country == 'New Zealand':
            site = 'trademe'
        elif country == 'Republic of Korea':
            site = 'coupang'
        else: #country == 'Switzerland'
            site = 'ricardo'

        # Find the row with the maximum Lifetime_exclude_session_cookie value
        #max_lifetime_row = data.loc[[data['Lifetime_exclude_session_cookie'].idxmax()]]
        max_lifetime_row = data[data['Page'].str.contains(site)]

        # If max_lifetime_row is empty, skip this file
        if max_lifetime_row.empty:
            continue

        max_lifetime_row.index = [country]

        # Add the DataFrame to the list
        df_list += [max_lifetime_row]

    # Concatenate all the DataFrames in the list
    max_lifetime_df = pd.concat(df_list)

    # Add the filenames as the first row
    max_lifetime_df.index.name = 'Country'
    max_lifetime_df.to_csv('avg_lifetime_for_top_shopping_web_in_each_country.csv')

if __name__ == "__main__":
    # Input argument check
    if len(sys.argv) < 2:
        directory = input("Please enter the directory path to pick top lifetime in each country: ")
    else:
        directory = sys.argv[1]
    create_max_lifetime_csv(directory)
