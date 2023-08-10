import pandas as pd
import glob
import sys
import os

def process_csv_files(directory):
    # Get all the csv files in the directory
    files = glob.glob(os.path.join(directory, "*_3rd_party.csv"))
    
    for csv_file in files:
        file_name = os.path.basename(csv_file)
        file_name_wo_suffix = file_name.split('_3rd_party.csv')[0]

        # Read each csv file
        df = pd.read_csv(csv_file)

        # Compute the average lifetime per page including and excluding session cookies
        avg_lifetime_include = df.groupby("Page")["Lifetime"].mean()
        avg_lifetime_exclude = df[df["session"] != True].groupby("Page")["Lifetime"].mean()

        # Count the number of cookies and session cookies per page
        num_cookies = df.groupby("Page")["Page"].count()
        #num_session_cookies = df[df["session"] == True].groupby("Page")["session"].count().fillna(0)
        num_session_cookies = df.groupby("Page")["session"].apply(lambda x: (x==True).sum()).fillna(0)

        # Merge the dataframes
        result = pd.concat([avg_lifetime_include, avg_lifetime_exclude, num_cookies, num_session_cookies], axis=1)

        # Rename the columns
        result.columns = ["Lifetime_include_session_cookie", "Lifetime_exclude_session_cookie", "number_of_cookie", "number_of_session_cookie"]

        # Convert the counts to integer
        result[["number_of_cookie", "number_of_session_cookie"]] = result[["number_of_cookie", "number_of_session_cookie"]].astype(int)

        # Sort the dataframe in descending order by Lifetime_exclude_session_cookie
        result.sort_values(by="Lifetime_exclude_session_cookie", ascending=False, inplace=True)

        # Save the result as a new csv file
        result.to_csv(f"avg_lifetime_by_web_for_{file_name_wo_suffix}.csv")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        directory = input("Please enter the directory which includes *_3rd_party.csv files: ")
    else:
        directory = sys.argv[1]

    process_csv_files(directory)
