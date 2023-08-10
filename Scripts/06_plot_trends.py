import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

def count_values(csv_path):
    df = pd.read_csv(csv_path)
    keys = ['httpOnly', 'secure', 'session']
    key_counts = {}
    for key in keys:
        if key in df.columns:
            counts = df[key].value_counts().to_dict()
            key_counts[key] = counts
        else:
            print(f"{key} does not exist in the dataframe")
    return key_counts

def plot_graphs(directory):
    group1_max_y_value = 0
    group2_max_y_value = 0
    csv_files = glob.glob(os.path.join(directory, "*_3rd_party.csv"))

    # Calculate y max values for the two groups
    for csv_file in csv_files:
        counts = count_values(csv_file)
        #total_sum = sum(counts[key].get(True, 0) + counts[key].get(False, 0) for key in ['httpOnly', 'secure', 'session'])
        total_sum = sum(counts[key].get(False, 0) for key in ['httpOnly', 'secure', 'session'])
        country_name  = os.path.basename(csv_file).split('_3rd_party.csv')[0].split('_')[-1]
        if country_name in ["All Countries", "Stricter Rule", "Less Stricter"]:
            group1_max_y_value = max(group1_max_y_value, total_sum)
        else:
            group2_max_y_value = max(group2_max_y_value, total_sum)

    # Plot the graphs using the appropriate y max value for each group
    for i, csv_file in enumerate(csv_files):
        counts = count_values(csv_file)
        country_name = os.path.basename(csv_file).split('_3rd_party.csv')[0].split('_')[-1]
        new_file_name = os.path.basename(csv_file).split('_3rd_party.csv')[0]
        #max_y_value = (group1_max_y_value+3000) if country_name in ["All Countries", "Stricter Rule", "Less Stricter"] else (group2_max_y_value+500)
        values = []
        labels = []
        colors = ['#FFC0CB', '#66CDAA', '#4682B4']
        x_ticks = [False, True]
        for key, key_count in counts.items():
            values.append([key_count.get(x_tick, 0) for x_tick in x_ticks])
            labels.append(key)
        x = np.arange(len(x_ticks))
        plt.figure(i, figsize=(8, 6))
        plt.stackplot(x, values, labels=labels, colors=colors)
        plt.xlabel("Values", fontsize = 14)
        plt.ylabel("Count", fontsize = 14)
        if country_name == "All Countries":
            plt.title('Cookie attributes and their trends \nin all countries', fontsize=16, fontweight='bold')
        #    plt.ylim(0, max_y_value)
        elif country_name == "Less Stricter":
            plt.title('Cookie attributes and their trends \nin less stricter countries', fontsize=16, fontweight='bold')
        #    plt.ylim(0, max_y_value)
        elif country_name == "Stricter Rule":
            plt.title('Cookie attributes and their trends \nin stricter countries', fontsize=16, fontweight='bold')
        #    plt.ylim(0, max_y_value)
        else:
            plt.title(f"Cookie attributes and their trends \nin {country_name}", fontsize = 16, fontweight = 'bold')
            #plt.ylim(0, max_y_value)
        plt.xticks(x, x_ticks, fontsize=12)
        plt.yticks(fontsize=12)
        plt.legend()
        plt.tight_layout()

        plt.savefig(f'{new_file_name}_attr_trends.png')
        #plt.show()
        plt.close()  # Add this line to close the figure


if __name__ == "__main__":
    import argparse
    import sys

    # Input argument check
    if len(sys.argv) < 2:
        dirname = input("Please enter the directory path which includes _3rd_paty.csv for creating the graph: ")
    else:
        dirname = sys.argv[1]

    plot_graphs(dirname)
