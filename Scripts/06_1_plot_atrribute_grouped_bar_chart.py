#    ax.bar(x - width/2, gdpr_like_false, width, color=colors_academic[0], edgecolor='black', hatch='//', linewidth=1, label='GDPR-like (False)')
#    ax.bar(x - width/2, gdpr_like_true, width, color=colors_academic[0], bottom=gdpr_like_false, label='GDPR-like (True)')
#    ax.bar(x + width/2, gdpr_ccpa_false, width, color=colors_academic[1], edgecolor='black', hatch='//', linewidth=1, label='GDPR&CCPA (False)')
#    ax.bar(x + width/2, gdpr_ccpa_true, width, color=colors_academic[1], bottom=gdpr_ccpa_false, label='GDPR&CCPA (True)')
#    
#    ax.set_xlabel('Attributes')
#    ax.set_ylabel('Counts')
#    ax.set_title('Cookie attributes in GDPR-like vs GDPR&CCPA countries')
#    ax.set_xticks(x)
#    ax.set_xticklabels(labels)
#    ax.legend()
#    
#    plt.tight_layout()
#    plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

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

def plot_grouped_bar_chart_final_updated(directory, save_filename="grouped_bar_chart.png"):
    #gdpr_like_file = os.path.join(directory, "All Countries_GDPR-like Countries_3rd_party.csv")
    #gdpr_ccpa_file = os.path.join(directory, "All Countries_GDPR&CCPA Countries_3rd_party.csv")
    gdpr_like_file = os.path.join(directory, "All Countries_GDPR-like Countries_3rd_party_only.csv")
    gdpr_ccpa_file = os.path.join(directory, "All Countries_GDPR&CCPA Countries_3rd_party_only.csv")
    
    gdpr_like_counts = count_values(gdpr_like_file)
    gdpr_ccpa_counts = count_values(gdpr_ccpa_file)
    
    labels = ['httpOnly', 'secure', 'session']
    x = np.arange(len(labels))
    width = 0.3

    gdpr_like_false = [gdpr_like_counts[key].get(False, 0) for key in labels]
    gdpr_like_true = [gdpr_like_counts[key].get(True, 0) for key in labels]
    gdpr_ccpa_false = [gdpr_ccpa_counts[key].get(False, 0) for key in labels]
    gdpr_ccpa_true = [gdpr_ccpa_counts[key].get(True, 0) for key in labels]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_academic = ['#7aa5b3', '#4b81bf']
    
    ax.bar(x - width/2 - 0.05, gdpr_like_false, width, color=colors_academic[0], edgecolor='black', hatch='//', linewidth=1, label='GDPR-like (False)')
    ax.bar(x - width/2 - 0.05, gdpr_like_true, width, color=colors_academic[0], bottom=gdpr_like_false, label='GDPR-like (True)')
    ax.bar(x + width/2 + 0.05, gdpr_ccpa_false, width, color=colors_academic[1], edgecolor='black', hatch='//', linewidth=1, label='GDPR/CCPA (False)')
    ax.bar(x + width/2 + 0.05, gdpr_ccpa_true, width, color=colors_academic[1], bottom=gdpr_ccpa_false, label='GDPR/CCPA (True)')
    
    ax.set_xlabel('Attributes')
    ax.set_ylabel('Counts')
    ax.set_title('Third party cookie attributes in GDPR-like vs GDPR/CCPA countries')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc='upper left', bbox_to_anchor=(1,1))
    #ax.yaxis.grid(True)
    plt.grid(axis='y')
    plt.gca().set_axisbelow(True)
    #ax.xaxis.grid(False)
    #ax.spines['right'].set_visible(False)
    #ax.spines['top'].set_visible(False)
    #ax.spines['bottom'].set_visible(False)
    #ax.spines['left'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(save_filename, bbox_inches='tight')
    plt.savefig('attribute_grouped_bar_chart.pdf', format='pdf', dpi=600)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python <script_name>.py /path/to/directory [optional_output_filename.png]")
        sys.exit(1)
    directory = sys.argv[1]
    save_filename = "grouped_bar_chart.png" if len(sys.argv) == 2 else sys.argv[2]
    plot_grouped_bar_chart_final_updated(directory, save_filename)
