import sys
import pandas as pd
import matplotlib.pyplot as plt

# Define the maximum width of the title (in characters)
title_max_width = 60

# Read CSV file
def read_csv_file(csv_file):
    try:
        data = pd.read_csv(csv_file)
        return data
    except FileNotFoundError:
        print("CSV file not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("Empty CSV file.")
        sys.exit(1)

def plot_horizontal_grouped_bar_graph_absolute_values(data, title):
    data = data.rename(columns={'Not set': 'Default'})
    categories = ['Strict', 'Lax', 'None', 'Default']
    #total_categories = data['Strict'] + data['Lax'] + data['None'] + data['Not set']
    y_labels = data['File']
    y_pos = range(len(y_labels))
    bar_width = 0.2

    colors=['#39A845', '#C1DB3C', '#DF5141', '#D4CACD']
    plt.figure(figsize=(12,6))

    for idx, category in enumerate(categories):
        values = data[category]
        position = [y - idx * bar_width for y in y_pos]
        plt.barh(position, values, color=colors[idx] , label=category, height=bar_width)

    plt.yticks([y - bar_width * 1.5 for y in y_pos], y_labels, fontsize=16)
    plt.xticks(fontsize=16)
    plt.xlabel('Number of Cookies', fontsize=16)
    plt.title(title, fontweight='bold', fontsize=16)
    plt.legend(loc='lower right', fontsize=14)
    plt.gca().invert_yaxis()
    plt.grid(axis='x')
    plt.gca().set_axisbelow(True)
    plt.tight_layout()
    output_file = f"{title}_abs.pdf"
    plt.savefig(output_file, format='pdf', dpi=600)
    plt.show()
    plt.close()

# Plot horizontal stacked bar graph using absolute values
def plot_horizontal_stacked_bar_graph_absolute_values(data, title):
    values_strict = data['Strict']
    values_lax = data['Lax']
    values_none = data['None']
    values_default = data['Not set']
    y_labels = data['File']
    y_pos = range(len(y_labels))
    plt.figure(figsize=(12,8))
    plt.barh(y_pos, values_strict, color='#39A845', label='Strict')
    plt.barh(y_pos, values_lax, left=values_strict, color='#C1DB3C', label='Lax')
    plt.barh(y_pos, values_none, left=values_strict + values_lax, color='#DF5141', label='None')
    plt.barh(y_pos, values_default, left=values_strict + values_lax + values_none, color='#D4CACD', label='Default')
    plt.yticks(y_pos, y_labels, fontsize=16)
    plt.xticks(fontsize=16)
    plt.xlabel('Number of Cookies', fontsize=16)
    plt.title(title, fontweight='bold', fontsize=16)
    plt.legend(loc='lower right', fontsize=14)
    plt.gca().invert_yaxis()
    plt.grid(axis='x')
    plt.gca().set_axisbelow(True)
    plt.tight_layout()
    output_file = f"{title}_abs.pdf"
    plt.savefig(output_file, format='pdf', dpi=600)
    plt.show()
    plt.close()

# Get input argument
if len(sys.argv) > 1:
    csv_file = sys.argv[1]
else:
    csv_file = input("Please enter the CSV file path: ")

# Terminate the program if the user does not input
if not csv_file:
    print("CSV file path is required.")
    sys.exit(1)

# Read the CSV file
data = read_csv_file(csv_file)

# Plotting the graphs using absolute values for specified and other files
data['File'] = data['File'].apply(lambda x: x.split('_')[-1])
data['File'] = data['File'].replace('GDPR-like Countries', 'GDPR-like Countries')
data['File'] = data['File'].replace('GDPR&CCPA Countries', 'GDPR&CCPA Countries')
specified_files_data = data[data['File'].isin(["All Countries", "GDPR-like Countries", "GDPR&CCPA Countries"])]
other_files_data = data[~data['File'].isin(["All Countries", "GDPR-like Countries", "GDPR&CCPA Countries"])]
#plot_horizontal_stacked_bar_graph_absolute_values(specified_files_data, "The Proportion of 'sameSite' Cookie Attributes by Rules Strictness")
plot_horizontal_grouped_bar_graph_absolute_values(specified_files_data, "The Proportion of 'sameSite' Cookie Attributes by Rules Strictness")
plot_horizontal_stacked_bar_graph_absolute_values(other_files_data, "The Proportion of 'sameSite' Cookie Attributes Across Different Countries")
