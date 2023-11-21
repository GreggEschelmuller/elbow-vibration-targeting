
import numpy as np
import matplotlib.pyplot as plt

# Define the parameters for two normal distributions
dist1_mean, dist1_std = 10, 2  # Mean and standard deviation for distribution 1
dist2_mean, dist2_std = 15, 3  # Mean and standard deviation for distribution 2

def sample_and_calculate(n):
    samples_dist1 = np.random.normal(dist1_mean, dist1_std, n)
    samples_dist2 = np.random.normal(dist2_mean, dist2_std, n)

    mean_dist1, std_dist1 = np.mean(samples_dist1), np.std(samples_dist1)
    mean_dist2, std_dist2 = np.mean(samples_dist2), np.std(samples_dist2)

    return (mean_dist1, std_dist1), (mean_dist2, std_dist2)

# Number of repetitions for each sample size
repetitions = 100

# Range of sample sizes
sample_sizes = range(1, 50)

# Storing results
results_dist1 = {n: {'means': [], 'stds': []} for n in sample_sizes}
results_dist2 = {n: {'means': [], 'stds': []} for n in sample_sizes}

# Sampling and calculating for each sample size and repetition
for n in sample_sizes:
    for _ in range(repetitions):
        result_dist1, result_dist2 = sample_and_calculate(n)

        results_dist1[n]['means'].append(result_dist1[0])
        results_dist1[n]['stds'].append(result_dist1[1])

        results_dist2[n]['means'].append(result_dist2[0])
        results_dist2[n]['stds'].append(result_dist2[1])

# Function to plot the results
def plot_results(results, true_mean, true_std, title):
    means = [np.mean(results[n]['means']) for n in sample_sizes]
    stds = [np.mean(results[n]['stds']) for n in sample_sizes]

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(sample_sizes, means, label='Estimated Mean')
    plt.hlines(true_mean, 1, 20, colors='r', linestyles='dashed', label='True Mean')
    plt.title(f'{title} - Means')
    plt.xlabel('Sample Size')
    plt.ylabel('Mean')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(sample_sizes, stds, label='Estimated Std Dev')
    plt.hlines(true_std, 1, 20, colors='r', linestyles='dashed', label='True Std Dev')
    plt.title(f'{title} - Standard Deviations')
    plt.xlabel('Sample Size')
    plt.ylabel('Standard Deviation')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Plotting the results for both distributions
plot_results(results_dist1, dist1_mean, dist1_std, 'Distribution 1')
plot_results(results_dist2, dist2_mean, dist2_std, 'Distribution 2')