import sys
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np
from urllib.parse import urlparse
import matplotlib.colors as mcolors

def draw_bar_graph(csvfile):
    data = pd.read_csv(csvfile)
    # Change unit from second to hour for Lifetime_exclude_session_cookie
    data['Lifetime_exclude_session_cookie'] = data['Lifetime_exclude_session_cookie'] / 3600

    # Extract netloc (domain name) from the 'Page' column
    data['Page'] = data['Page'].apply(lambda x: urlparse('http://' + x).netloc)

    # Combine 'Domain' and 'Country' column
    data['Domain (Country)'] = data['Page'] + " (" + data['Country'] + ")"

    # Sort data in descending order
    data = data.sort_values(by='Lifetime_exclude_session_cookie', ascending=False)

    # Calculate number of unique countries
    num_countries = len(data['Country'].unique())

    lighter_gold = (250/255, 210/255, 50/255)

    # Create a custom color gradient from "magenta" to a transparent version of the color
    #start_color = 'palegoldenrod'
    start_color = lighter_gold
    #colors = [mcolors.to_rgba(start_color, alpha=i/(num_countries-1)) for i in range(num_countries)]
    min_alpha = 0.5  # Set the minimum alpha value
    colors = [mcolors.to_rgba(start_color, alpha=min_alpha + (1-min_alpha)*i/(num_countries-1)) for i in range(num_countries)]
    colors = list(reversed(colors))

    # Draw the graph
    fig, ax1 = plt.subplots(figsize=(16,10))
    ax2 = ax1.twiny()  # Create second x-axis

    ax1.barh(y=data['Domain (Country)'], width=data['Lifetime_exclude_session_cookie'], color=colors)
    #ax1.barh(y=data['Country'], width=data['Lifetime_exclude_session_cookie'], color=colors)
    ax1.set_xlabel('Life cycle (hours)')
    ax1.set_ylabel('Top-Level Domain (Country)')
    #ax1.set_ylabel('Country')
    ax1.set_title('Average life cycle of cookies on top shopping websites\n in each country without session cookies', fontsize=16, fontweight='bold', y=1.07)

    # Add a tick every 720 hours on the x-axis
    max_hour = np.max(data['Lifetime_exclude_session_cookie'])
    x_ticks = np.arange(0, max_hour, 720)
    ax1.set_xticks(x_ticks)

    # Add month labels on the second x-axis
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels([f'{int(x/720)}' for x in x_ticks])
    ax2.set_xlabel('Life cycle (months)')

    # grid line 표현
    ax1.grid(axis='x')

    ax1.invert_yaxis()
    plt.subplots_adjust(left=0.15, right=0.85)  # Adjust the padding for x-axis labels
    plt.tight_layout()
    plt.savefig('avg_lifetime_for_top_shopping_web_in_each_country.png')
    plt.show()

if __name__ == "__main__":
    csvfile = 'avg_lifetime_for_top_shopping_web_in_each_country.csv'
    draw_bar_graph(csvfile)
