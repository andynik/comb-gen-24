# Correlation analysis

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the Parquet file
df = pd.read_parquet('path-to-dataset/combinatorics4_final_test_1000.parquet')
# df = pd.read_parquet('path-to-dataset/combinatorics_5583_final.parquet')


# List of columns including 'answer' and the variations to compare
columns_to_compare = ['original_ans', 'fictional_ans', 'adversarial_ans', 'contdis_ans']

# Initialize a dictionary to store comparison results
comparison_results = {}

# Compare 'answer' with each column including itself
for col in columns_to_compare:
    comparison_results[col] = (df['answer'] == df[col]).astype(int)

# Create a DataFrame with the results
results_df = pd.DataFrame(comparison_results)

# Compute the correlation matrix for the comparison results
correlation_matrix = results_df.corr()

# Plot a heatmap of the correlation matrix
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap Including Answer Column')
plt.yticks(rotation=0)  # Set y-tick rotation for better readability
plt.xticks(rotation=45, ha='right')  # Set x-tick rotation for better readability
plt.tight_layout()

# Show the plot
plt.show()