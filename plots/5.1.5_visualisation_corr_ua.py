import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load your data
df = pd.read_parquet('path-to-dataset/combinatorics4_final_test_1000.parquet')

# List of columns for comparison
columns_to_compare = ['original_ans', 'fictional_ans', 'adversarial_ans', 'contdis_ans']

# Initialize a dictionary to store comparison results
comparison_results = {}

# Compare 'answer' with each column
for col in columns_to_compare:
    comparison_results[col] = (df['answer'] == df[col]).astype(int)

# Create a DataFrame with the results
results_df = pd.DataFrame(comparison_results)

# Compute the correlation matrix for the comparison results
correlation_matrix = results_df.corr()

# Create a heatmap with a suitable colormap for grayscale printing
plt.figure(figsize=(8, 6))

# Use a colormap that is distinguishable in grayscale
sns.heatmap(correlation_matrix, annot=True, cmap='Greys', fmt=".2f",
            cbar_kws={"shrink": .8}, linewidths=0.5, linecolor='gray')

plt.title('Теплова карта кореляції між варіаціями задач')
plt.yticks(rotation=0)  # Y-ticks label rotation for readability
plt.xticks(rotation=45, ha='right')  # X-ticks label rotation
plt.tight_layout()  # Adjust layout for better fit

# Display the plot
plt.show()