import random
import pandas as pd

# Define your target and vibration conditions
targets = [8]
vibrations = [0, 0, 0, 1, 2, 3]

# Number of cycles you want to create
n_cycles = 30  # Change this to the desired number of cycles

# Initialize a list to store the randomized trials
all_trials = []

# Generate n_cycles with randomized trials
for _ in range(n_cycles):
    # Create a list of trial orders for the current cycle
    cycle_trials = []

    # Randomly shuffle the target and vibration conditions
    random_targets = random.sample(targets, len(targets))
    random_vibrations = random.sample(vibrations, len(vibrations))

    # Create all possible combinations of targets and vibrations
    trials = [
        (target, vibration)
        for target in random_targets
        for vibration in random_vibrations
    ]

    # Shuffle the order of trials within the cycle
    random.shuffle(trials)

    # Add the randomized trials for the current cycle to the list
    cycle_trials.extend(trials)

    # Add the current cycle's trials to the overall list
    all_trials.extend(cycle_trials)

# Create a DataFrame to store the randomized trials
trial_df = pd.DataFrame(all_trials, columns=["Target", "Vibration"])

# Write the DataFrame to an Excel file
output_excel_file = "../../randomized_trials.xlsx"
trial_df.to_excel(output_excel_file, index=False)
