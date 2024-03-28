import matplotlib as mpl
mpl.rcParams["axes.spines.right"] = False
mpl.rcParams["axes.spines.top"] = False

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

ax_list = [[0,0], [0,1], [0,2],
           [1,0], [1,1], [1,2],
           [2,0], [2,1], [2,2],
           [3,0], [3,1], [3,2],
           [4,0], [4,1], [4,2],]
fig, axes = plt.subplots(5, 3, figsize=(20, 10))  # Create a 3x5 grid of subplots
fig.tight_layout(pad=3.0)  # Add space between plots for clarity
for i in range(1, 16):  # Change 9 to a higher number if you have more participants
    file_name = f'data/p{i}/p{i}_main.csv'  # Constructs the file name
    df = pd.read_csv(file_name)  # Reads the file into a DataFrame
    df['participant'] = i  # Adds the participant number
    df = df.drop('block', axis=1)  # Drops the column you don't need
    filtered_data = df[(df["move_times"] > 0.4) & (df['mean_velocity'] > 20)]
    # fig, ax = plt.subplots()
    # sns.stripplot(x='vibration', y='error', data=df, ax=ax, hue="vibration", alpha = 0.2, palette='pastel')
    # sns.pointplot(x='vibration', y='error', data=df, ax=ax, hue="vibration", palette='pastel')
    # ax.legend_.remove()
    # ax.set_xlabel('')
    # ax.set_xticklabels(['No Vibration', 'Dual Vibration', 'Triceps Vibration', 'Biceps Vibration'])
    # ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
    # ax.set_title("Vibration induced error scores")
    # fig.savefig(f'results/p{i}_error_plot.png', dpi=1000)

    # Loop over all participants and plot their data
    # ax = axes[ax_list[i]]  # Get the specific subplot axis
    sns.stripplot(x='vibration', y='error', data=filtered_data, ax=axes[ax_list[i-1][0], ax_list[i-1][1]], hue="vibration", alpha = 0.2, palette='pastel')
    sns.pointplot(x='vibration', y='error', data=filtered_data, ax=axes[ax_list[i-1][0], ax_list[i-1][1]], hue="vibration", palette='pastel')
    axes[ax_list[i-1][0], ax_list[i-1][1]].legend_.remove()
    axes[ax_list[i-1][0], ax_list[i-1][1]].set_xlabel('')
    axes[ax_list[i-1][0], ax_list[i-1][1]].set_xticklabels(['None', 'Dual', 'Triceps', 'Biceps'])
    axes[ax_list[i-1][0], ax_list[i-1][1]].set_title(f"Participant {i}")
    axes[ax_list[i-1][0], ax_list[i-1][1]].axhline(0, color='black', linewidth=0.5, linestyle='--')
    

    # Adjust layout to make room for titles, labels, etc.
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.5, wspace=0.4)
fig.savefig(f'results/all_error_plots.png', dpi=1000)
# plt.show()