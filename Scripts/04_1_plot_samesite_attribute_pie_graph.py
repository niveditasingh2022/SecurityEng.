import sys
import pandas as pd
import matplotlib.pyplot as plt
import textwrap

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

# For loop through each row to plow the graph
for i, row in data.iterrows():
    # Prepare data for plotting the graph
    file = row['File']
    total_cookies = row['Total Cookies']
    strict = row['Strict']
    lax = row['Lax']
    none = row['None']
    missing = row['Not set']

    # Set colors
    colors = ['#39A845', '#C1DB3C', '#DF5141', '#D4CACD'] 

    # Plot the graph
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot the pie chart and set color, pattern for each section
    wedges, text, autotext = ax.pie([strict, lax, none, missing],
                                    explode=(0.005, 0.005, 0.005, 0.005),
                                    colors=colors,
                                    startangle=90,
                                    autopct=lambda pct: f"{abs(pct):.1f}%\n({int(abs(pct/100*total_cookies))})",
                                    textprops={'color': 'black', 'fontsize': 14},
                                    pctdistance=0.85)

    # Adjust position
    for t in autotext:
        t.set_position([0.8 * v for v in t.get_position()])

    # Display lable for each section
    labels = ['Strict', 'Lax', 'None', 'Default']
    ax.legend(wedges, labels, loc='upper right', bbox_to_anchor=(1.1, 1))


    # Set title of the graph
    if file == "All Countries":
        #title = '"SameSite" cookie attribute proportion (France, Germany, Italy, the Netherlands, Poland, Spain, Sweden, the USA, Australia, Brazil, Canada, Chile, India, Japan, New Zealand, Republic of Korea, and Switzerland)'
        title = '"SameSite" cookie attribute proportion (France, Germany, Italy, Netherlands, Poland, Spain, Sweden, USA, Australia, Brazil, Canada, Chile, India, Japan, New Zealand, Republic of Korea, and Switzerland)'
        ax.set_title(textwrap.fill(title, title_max_width), fontweight='bold', fontsize=16)
    elif file == "All Countries_Less Stricter":
        #title = '"SameSite" cookie attribute proportion (Australia, Brazil, Canada, Chile, India, Japan, New Zealand, Republic of Korea, and Switzerland)'
        title = '"SameSite" cookie attribute proportion (Australia, Brazil, Canada, Chile, India, Japan, New Zealand, Republic of Korea, and Switzerland)'
        ax.set_title(textwrap.fill(title, title_max_width), fontweight='bold', fontsize=16)
    elif file == "All Countries_Stricter Rule":
        #title = '"SameSite" cookie attribute proportion (France, Germany, Italy, the Netherlands, Poland, Spain, Sweden, and the USA)'
        title = '"SameSite" cookie attribute proportion (France, Germany, Italy, Netherlands, Poland, Spain, Sweden, and USA)'
        ax.set_title(textwrap.fill(title, title_max_width), fontweight='bold', fontsize=16)
    else:
        country = file.split("_")[-1]
        ax.set_title(f'"SameSite" cookie attribute proportion ({country})', fontweight='bold', fontsize=16)

    # Save the graph
    plt.tight_layout()
    output_file = f"{file}_samesite_attribute_pie_chart.pdf"
    plt.savefig(output_file, format='pdf', dpi=600)
    plt.close()
