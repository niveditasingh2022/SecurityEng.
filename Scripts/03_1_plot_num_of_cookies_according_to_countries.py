import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import patches
import matplotlib as mpl

def darken_color(color, degree=0.5):
    """
    This function darkens the input color.

    Parameters:
    - color: the original color
    - degree: the degree of darkness (1 - degree of lightness)

    Returns:
    - the darkened color
    """
    try:
        c = mcolors.cnames[color]
    except:
        c = color
    c = mcolors.to_rgb(c)
    #c = (1 - degree) * (1 - 1) + degree * c  # to darken, can replace 1 with 0
    c = [max(0, x - degree) for x in c]
    return c

# Set the hatch linewidth globally
mpl.rcParams['hatch.linewidth'] = 1

# Load the CSV data
data = pd.read_csv('./num_of_3rd_party_cookies.csv')

# Display the first few rows of the dataframe
data.head()

# Split the 'File' column into 'Rule_Strictness' and 'Country'
rows_to_remove = ['All Countries', 'All Countries_GDPR-like Countries', 'All Countries_GDPR&CCPA Countries'] 
data = data[~data['File'].isin(rows_to_remove)] # Remove the rows we don't want
data['Rule_Strictness'] = data['File'].apply(lambda x: x.split('All Countries_', 1)[-1].split('_', 1)[0])
data['Country'] = data['File'].apply(lambda x: x.split('All Countries_', 1)[-1].split('_', 1)[-1].split('_')[-1])

# Get the unique contries
unique_countries = data['Country'].unique()

# Create darker versions of the original colors
dark_blue = darken_color('#4b81bf', 0.1)
dark_green = darken_color('#39A845', 0.4)

# Choose more academically appropriate colors from the provided palette
colors_academic = ['#7aa5b3', '#4b81bf']  # lightblue+0.2 and Blue

# Get the indices for the two groups of countries
indices_less_stricter = [i for i, country in enumerate(unique_countries) if 'GDPR-like Countries' in data[data['Country'] == country]['Rule_Strictness'].values]
indices_stricter_rule = [i for i, country in enumerate(unique_countries) if 'GDPR&CCPA Countries' in data[data['Country'] == country]['Rule_Strictness'].values]

# Plotting the data
fig, ax = plt.subplots(figsize=(12, 8))
for rule_strictness, color, dark_color in zip(['GDPR-like Countries', 'GDPR&CCPA Countries'], colors_academic, [dark_blue, dark_green]):
    
    # Filter the data based on the rule strictness
    filtered_data = data[data['Rule_Strictness'] == rule_strictness]
    
    ## Create a bar plot for the filtered data
    #ax.bar(filtered_data['Country'], filtered_data['Total Cookies'], color=color, edgecolor=color, label=f'{rule_strictness} - Total Cookies')
    #ax.bar(filtered_data['Country'], filtered_data['3rd Party Cookies'], color=color, edgecolor= 'black', hatch='/////', linewidth=1, label=f'{rule_strictness} - Third Party Cookies')
    bars1 = ax.bar(filtered_data['Country'], filtered_data['Total Cookies'], color=color, edgecolor=color, label=f'{rule_strictness} - Total Cookies')
    bars2 = ax.bar(filtered_data['Country'], filtered_data['3rd Party Cookies'], color=color, edgecolor='black', hatch='//', linewidth=1, label=f'{rule_strictness} - Third Party Cookies')
    # Annotating the percentage of 3rd party cookies
    for bar1, bar2 in zip(bars1, bars2):
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        percentage_3rd_party = (height2 / height1) * 100
        percentage_remaining = 100 - percentage_3rd_party
        #ax.annotate(f'{percentage_3rd_party:.2f}%', xy=(bar2.get_x() + bar2.get_width() / 2, height2 / 2), ha='center', va='center', fontsize=16, color='black')
        #ax.annotate(f'{percentage_remaining:.2f}%', xy=(bar1.get_x() + bar1.get_width() / 2, (height1 + height2) / 2), ha='center', va='center', fontsize=16, color='white')
        #ax.annotate(f'{percentage_remaining:.2f}%', xy=(bar1.get_x() + bar1.get_width() / 2, height1 - 20), ha='center', va='center', fontsize=16, color='black')
        percentage = (height2 / height1) * 100
        ax.annotate(f'{percentage:.2f}%', xy=(bar2.get_x() + bar2.get_width() / 2, height2), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=12, color='black')


# Formatting the plot
plt.title('Proportion of third party cookies in total number of cookies', fontsize=16, fontweight='bold', y=1.02)
plt.xlabel('Countries in our dataset', fontsize=16)
plt.ylabel('Number of cookies', fontsize=16)
plt.xticks(rotation=45, ha='right', fontsize=16)
plt.yticks(fontsize=16)
plt.legend(loc='upper right', prop={'size': 12})
#plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add a grid

# Display the plot
plt.grid(axis='y')
plt.gca().set_axisbelow(True)
plt.tight_layout()

#plt.savefig('num_of_cookies_according_to_countries.png')
plt.savefig('num_of_cookies_according_to_countries.pdf', format='pdf', dpi=600)
plt.show()