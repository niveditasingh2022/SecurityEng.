import os
import glob
import pandas as pd

# Get the list of all *_3rd_party.csv files in the current directory
csv_files = glob.glob('*_3rd_party.csv')

for csv_file in csv_files:
    # Load CSV data
    df = pd.read_csv(csv_file)
    
    # Filter rows where '3rd_party' is True
    third_party_only_data = df[df['3rd_party'] == True]
    
    # Generate the output file name
    output_filename = csv_file.replace('_3rd_party.csv', '_3rd_party_only.csv')
    
    # Save the filtered data to the new file
    third_party_only_data.to_csv(output_filename, index=False)
