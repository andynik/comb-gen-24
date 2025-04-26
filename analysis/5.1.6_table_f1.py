import pandas as pd
import numpy as np

# Load the Parquet file
# df = pd.read_parquet('dataset_5583/combinatorics_5583_final.parquet')
df = pd.read_parquet('dataset_1k_test/combinatorics4_final_test_1000.parquet')

# List of columns for the variations
columns_to_compare = ['fictional_ans', 'adversarial_ans', 'contdis_ans']

# Column for the original answers
original_column = 'original_ans'

# Get the total number of problems
n_problems = len(df)

# Calculate the percentage of correct answers for each variation
correct_percentages = {col: (df['answer'] == df[col]).sum() / n_problems for col in columns_to_compare}

# Initialize a dictionary to store correlation with the original answers
correlation_to_original = {}

# Compute correlation with the original answers
for col in columns_to_compare:
    # Create binary columns for comparison with original_ans
    original_correct = (df[original_column] == df['answer']).astype(int)
    variation_correct = (df[col] == df['answer']).astype(int)
    # Calculate correlation between original and each variation
    correlation = np.corrcoef(original_correct, variation_correct)[0, 1]
    correlation_to_original[col] = correlation

# Calculate F1-score
f1_composite_scores = {}
for col in columns_to_compare:
    precision = correct_percentages[col]
    recall = correlation_to_original[col]
    # If the sum is zero, set F1 to zero
    if precision + recall > 0:
        f1 = 2 * (precision * recall) / (precision + recall)
    else:
        f1 = 0
    f1_composite_scores[col] = f1

# Create a DataFrame with the results
composite_df = pd.DataFrame({
    'Variation': columns_to_compare,
    'Correct %': list(correct_percentages.values()),
    'Correlation with Original': list(correlation_to_original.values()),
    'F1 Composite Score': list(f1_composite_scores.values())
})

# Print the results table
print("Composite Metrics using F1-Score:")
print(composite_df)

# Generate LaTeX code for the table
latex_code = composite_df.to_latex(index=False, float_format="%.3f")
print("\nLaTeX Table Code:")
print(latex_code)