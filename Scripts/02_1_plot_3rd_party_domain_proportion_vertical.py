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

csv_files = glob.glob(os.path.join(directory_path, '*_3rd_party.csv'))

for csv_file in csv_files:
    # Get the leaf_file_name from the input CSV file path
    base_name = os.path.basename(csv_file)  # Get the file name with extension
    file_name_without_suffix = base_name.split('_3rd_party.csv')[0]  # Remove the suffix

    # Split the string into parts based on '_'
    parts = file_name_without_suffix.split('_')

    # leaf_file_name is the last part after splitting
    leaf_file_name = parts[-1]

    # Load CSV data
    df = pd.read_csv(csv_file)

    # Filter rows where '3rd_party' is True
    third_party_true_data = df[df['3rd_party'] == True]

    # Count the occurrence of each 'cookie_domain'
    domain_counts = third_party_true_data['cookie_domain'].value_counts()
    total_third_party_true = len(third_party_true_data)
    cookie_domain_ratio = domain_counts / total_third_party_true
    sorted_ratio = cookie_domain_ratio.sort_values(ascending=False)
    top_domains = sorted_ratio[:20] # Select top 20

    # Create a dataframe with domain_counts and labels
    domain_counts_df = pd.DataFrame({'Cookie Domain': domain_counts.index, 'Count': domain_counts.values})

    # Save domain_counts and labels to CSV file
    #print("Original csv_file:", csv_file)
    #print("After splitting:", csv_file.split('.')[0])
    #print("Generated filename:", csv_file.split('.')[0] + '_domain_counts.csv')
    #print("Original csv_file:", csv_file)
    #print("After splitting:", os.path.splitext(csv_file)[0])
    #print("Generated filename:", os.path.splitext(csv_file)[0] + '_domain_counts.csv')
    #domain_counts_df.to_csv(csv_file.split('.')[0] + '_domain_counts.csv', index=False)
    domain_counts_df.to_csv(os.path.splitext(csv_file)[0] + '_domain_counts.csv', index=False)


    # Define a refined color palette based on filename_without_suffix and leaf_file_name
    if 'GDPR&CCPA Countries' in file_name_without_suffix:
        refined_color_palette = ['#4b81bf']
    elif 'GDPR-like Countries' in file_name_without_suffix:
        refined_color_palette = ['#7aa5b3']
    elif leaf_file_name == 'All Countries':
        refined_color_palette = ['#18418c']
    else:
        refined_color_palette = ['#4b81bf']  # Default color

    # Plotting
    plt.figure(figsize=(12, 8))
    #fig,ax = plt.subplots(figsize=(12, 8))
    bar_plot = top_domains.sort_values(ascending=False).plot(kind='bar', color=refined_color_palette)
    if leaf_file_name == "All Countries":
        plt.title(f'Top {len(top_domains)} third party cookies in all countries', fontsize=16, fontweight='bold')
        plt.ylim(0, 0.06) # Set y-axis limit to 6%
    elif leaf_file_name == "GDPR-like Countries":
        plt.title(f'Top {len(top_domains)} third party cookies in GDPR-like countries', fontsize=16, fontweight='bold')
        plt.ylim(0, 0.06) # Set y-axis limit to 6%
    elif leaf_file_name == "GDPR&CCPA Countries":
        plt.title(f'Top {len(top_domains)} third party cookies in GDPR/CCPA countries', fontsize=16, fontweight='bold')
        plt.ylim(0, 0.06) # Set y-axis limit to 6%
    else:
        plt.title(f'Top {len(top_domains)} third party cookies in ' + leaf_file_name, fontsize=16, fontweight='bold')
        #plt.ylim(0, 0.50) # Set y-axis limit to 50%

    plt.xlabel('Third parties', fontsize=16)
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
    plt.savefig(file_name_without_suffix + '_domain_proportion_vertical_graph.pdf', format='pdf', dpi=600)
    plt.close()