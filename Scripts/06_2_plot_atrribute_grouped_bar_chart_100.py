import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def compute_ratios(csv_path):
    df = pd.read_csv(csv_path)
    keys = ['httpOnly', 'secure', 'session']
    key_ratios = {}
    for key in keys:
        if key in df.columns:
            total = len(df[key])
            counts = df[key].value_counts().to_dict()
            ratios = {k: v/total for k, v in counts.items()}
            key_ratios[key] = ratios
        else:
            print(f"{key} does not exist in the dataframe")
    return key_ratios

def plot_grouped_bar_chart_ratios_updated(directory):
    gdpr_like_file = os.path.join(directory, "All Countries_GDPR-like Countries_3rd_party_only.csv")
    gdpr_ccpa_file = os.path.join(directory, "All Countries_GDPR&CCPA Countries_3rd_party_only.csv")
    
    gdpr_like_ratios = compute_ratios(gdpr_like_file)
    gdpr_ccpa_ratios = compute_ratios(gdpr_ccpa_file)
    
    labels = ['httpOnly', 'secure', 'session']
    x = np.arange(len(labels))
    width = 0.3

    gdpr_like_false = [gdpr_like_ratios[key].get(False, 0) for key in labels]
    gdpr_like_true = [gdpr_like_ratios[key].get(True, 0) for key in labels]
    gdpr_ccpa_false = [gdpr_ccpa_ratios[key].get(False, 0) for key in labels]
    gdpr_ccpa_true = [gdpr_ccpa_ratios[key].get(True, 0) for key in labels]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors_academic = ['#7aa5b3', '#4b81bf']
    
    ax.bar(x - width/2 - 0.05, gdpr_like_false, width, color=colors_academic[0], edgecolor='black', hatch='//', linewidth=1, label='GDPR-like (False)')
    ax.bar(x - width/2 - 0.05, gdpr_like_true, width, color=colors_academic[0], bottom=gdpr_like_false, label='GDPR-like (True)')
    ax.bar(x + width/2 + 0.05, gdpr_ccpa_false, width, color=colors_academic[1], edgecolor='black', hatch='//', linewidth=1, label='GDPR&CCPA (False)')
    ax.bar(x + width/2 + 0.05, gdpr_ccpa_true, width, color=colors_academic[1], bottom=gdpr_ccpa_false, label='GDPR&CCPA (True)')
    
    ax.set_xlabel('Attributes')
    ax.set_ylabel('Ratio')
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
    plt.savefig('attribute_grouped_bar_chart_prop.pdf', format='pdf', dpi=600)
    plt.show()

if __name__ == "__main__":
    directory = input("Enter the directory path where the CSV files are located: ")
    plot_grouped_bar_chart_ratios_updated(directory)
    