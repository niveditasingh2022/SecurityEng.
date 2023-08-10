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

# Plot horizontal stacked bar graph using absolute values
def plot_horizontal_stacked_bar_graph(data, title):
    # Extracting ratios
    total_categories = data['Strict'] + data['Lax'] + data['None'] + data['Not set']
    ratios_strict = data['Strict'] / total_categories
    ratios_lax = data['Lax'] / total_categories
    ratios_none = data['None'] / total_categories
    ratios_default = data['Not set'] / total_categories
    y_labels = data['File']
    y_pos = range(len(y_labels))
    
    plt.figure(figsize=(12, 8))
    plt.barh(y_pos, ratios_strict, color='#39A845', label='Strict')
    plt.barh(y_pos, ratios_lax, left=ratios_strict, color='#C1DB3C', label='Lax')
    plt.barh(y_pos, ratios_none, left=ratios_strict + ratios_lax, color='#DF5141', label='None')
    plt.barh(y_pos, ratios_default, left=ratios_strict + ratios_lax + ratios_none, color='#D4CACD', label='Default')
    
    # Adding percentage annotations to the bars
    for i, value in enumerate(y_pos):
        plt.text(ratios_strict.iloc[i] / 2 - 0.02, value, f'{ratios_strict.iloc[i] * 100:.1f}%', va='center', ha='center')
        plt.text(ratios_strict.iloc[i] + ratios_lax.iloc[i] / 2 - 0.02, value, f'{ratios_lax.iloc[i] * 100:.1f}%', va='center', ha='center')
        plt.text(ratios_strict.iloc[i] + ratios_lax.iloc[i] + ratios_none.iloc[i] / 2, value, f'{ratios_none.iloc[i] * 100:.1f}%', va='center', ha='center')
        plt.text(ratios_strict.iloc[i] + ratios_lax.iloc[i] + ratios_none.iloc[i] + ratios_default.iloc[i] / 2, value, f'{ratios_default.iloc[i] * 100:.1f}%', va='center', ha='center')
    
    plt.yticks(y_pos, y_labels)
    plt.xlabel('Proportion of Cookies')
    plt.title(title[:title_max_width], fontweight='bold')
    plt.legend(loc='lower right')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
    plt.close()

def plot_and_save_table(data, columns, title, save_path):
    # Updating the DataFrame with the new column label 'Country'
    data = data.rename(columns={columns[0]: 'Country'})
    columns[0] = 'Country'
    # Extracting the specified columns and creating table rows
    table_data = data[columns].copy()
    table_rows = [list(row) for row in table_data.values]
    col_labels = list(table_data.columns)

    # Plotting the table
    fig, ax = plt.subplots(figsize=(8, len(table_rows) * 0.3))
    ax.axis('off')
    ax.table(cellText=table_rows, colLabels=col_labels, cellLoc='center', loc='center', colColours=['lightgray']*len(col_labels))
    
    # Saving and displaying the table
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0.1)
    plt.show()
    plt.close()

def main():
    # Read the CSV file
    csv_file = 'path/to/your/csv/file.csv'
    data = read_csv_file(csv_file)

    # Plotting the bar graph
    plot_horizontal_stacked_bar_graph(data, "Your Title Here")

    # Preparing and saving the tables
    total_categories = data['Strict'] + data['Lax'] + data['None'] + data['Not set']
    data['Strict (%)'] = (data['Strict'] / total_categories * 100).round(1)
    data['Lax (%)'] = (data['Lax'] / total_categories * 100).round(1)
    data['None (%)'] = (data['None'] / total_categories * 100).round(1)
    data['Not set (%)'] = (data['Not set'] / total_categories * 100).round(1)
    absolute_columns = ['File', 'Strict', 'Lax', 'None', 'Not set']
    percentage_columns = ['File', 'Strict (%)', 'Lax (%)', 'None (%)', 'Not set (%)']
    plot_and_save_table(data, absolute_columns, "Absolute Values", "absolute_values.png")
    plot_and_save_table(data, percentage_columns, "Percentage Values", "percentage_values.png")

if __name__ == "__main__":
    main()
