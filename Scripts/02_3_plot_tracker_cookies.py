from matplotlib.ticker import PercentFormatter
import os
import pandas as pd
import matplotlib.pyplot as plt
import sys
import glob

# Input argument check
if len(sys.argv) < 2:
    directory_path = input("Please enter the directory path which includes _3rd_party.csv files for creating the graph: ")
else:
    directory_path = sys.argv[1]

csv_files = glob.glob(os.path.join(directory_path, 'tracker_domains.csv'))

for csv_file in csv_files:
    # Get the leaf_file_name from the input CSV file path
    file_name = os.path.basename(csv_file)  # Get the file name with extension
    file_name = file_name.split('.csv')[0]  # Remove the suffix

    # Load CSV data
    df = pd.read_csv(csv_file)

    # Count the occurrence of each 'cookie_domain'
    domain_counts = df['cookie_domain'].value_counts()
    total_third_party_true = len(df)
    cookie_domain_ratio = domain_counts / total_third_party_true
    sorted_ratio = cookie_domain_ratio.sort_values(ascending=False)
    top_domains = sorted_ratio[:20] # Select top 20

    # Create a dataframe with domain_counts and labels
    domain_counts_df = pd.DataFrame({'Cookie Domain': domain_counts.index, 'Count': domain_counts.values})

    # Define a refined color palette based on filename
    if 'GDPR&CCPA Countries' in file_name:
        refined_color_palette = ['#4b81bf']
    elif 'GDPR-like Countries' in file_name:
        refined_color_palette = ['#7aa5b3']
    elif file_name == 'All Countries':
        refined_color_palette = ['#18418c']
    else:
        refined_color_palette = ['#4b81bf']  # Default color

    # Plotting
    plt.figure(figsize=(12, 8))
    #fig,ax = plt.subplots(figsize=(12, 8))
    bar_plot = top_domains.sort_values(ascending=False).plot(kind='bar', color=refined_color_palette)
    plt.title(f'Top 20 tracker cookies among third-party cookies', fontsize=16, fontweight='bold')
    plt.ylim(0, 0.07) # Set y-axis limit to 6%

    plt.xlabel('Tracker Cookies', fontsize=16)
    plt.xticks(rotation=45, ha='right', fontsize=16)  # Rotate x-labels by 45 degrees
    plt.subplots_adjust(bottom=0.3)  # Adjust the space at the bottom
    plt.ylabel('Proportion\n (Number of cookies)', fontsize=16)
    plt.yticks(fontsize=16)
    plt.grid(False)

    #for i, v in enumerate(top_domains.values):
    #    plt.text(i, v, str(round(v*100, 2)) + '%', va='bottom', ha='center', color='black', fontsize=12)
    for i, (domain, v) in enumerate(top_domains.items()):
        cookie_count = domain_counts[domain]
        plt.text(i, v, str(round(v*100, 2)) + '%', va='bottom', ha='center', color='black', fontsize=12)
        # plt.text(i, v - 0.002, '(' + str(cookie_count)+')', va='bottom', ha='center', color='black', fontsize=12)  # Adjusted position for the cookie count text

    # Show the plot
    # plt.show()

    plt.gca().yaxis.set_major_formatter(PercentFormatter(1)) # Convert y-axis values to percentage

    #plt.grid(True)
    plt.grid(axis='y')
    plt.gca().set_axisbelow(True)
    plt.tight_layout()
    # Save the figure
    plt.savefig(file_name + '.pdf', format='pdf', dpi=600)
    plt.close()