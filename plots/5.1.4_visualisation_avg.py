import pandas as pd
import matplotlib.pyplot as plt

# Load the Parquet file
df = pd.read_parquet('path-to-dataset/combinatorics4_final_test_1000.parquet')
# df = pd.read_parquet('path-to-dataset/combinatorics_5583_final.parquet')


# List of the columns to compare with 'answer'
compare_columns = ['original_ans', 'fictional_ans', 'adversarial_ans', 'contdis_ans']

# Initialize a dictionary to store comparison results
comparison_results = {}

# Compare 'answer' with each column in compare_columns
for col in compare_columns:
    comparison_results[col] = (df['answer'] == df[col]).astype(int)

# Create a DataFrame with the results
results_df = pd.DataFrame(comparison_results)

# Calculate the total number of entries
total_entries = len(df)

# Calculate the percentage of correct answers for each variation
percentage_correct = (results_df.sum() / total_entries) * 100

# Calculate the number of variations that solve each problem correctly
solved_counts = results_df.sum(axis=1)

# Count how many problems were solved by 0, 1, 2, 3, or 4 variations
solved_distribution = solved_counts.value_counts().sort_index()

# Set up the subplot grid with different width ratios
fig, axes = plt.subplots(1, 2, figsize=(12, 6), gridspec_kw={'width_ratios': [3, 1]})

# Adjust space between plots
plt.subplots_adjust(wspace=0.2)

# Colors for the first plot
colors = ['blue', 'green', 'red', 'purple']

# Add horizontal grid lines
axes[0].yaxis.grid(True, linestyle='--', linewidth=0.7, color='gray')

# Plot 1: Percentage of Correct Answers
axes[0].bar(percentage_correct.index, percentage_correct.values, color=colors)
axes[0].set_xlabel('Variation', fontsize=12)
axes[0].set_ylabel('Percentage of Correct Answers', fontsize=12)
# axes[0].set_title('Percentage of Problems Solved Correctly per Variation', fontsize=16)

# Custom labels for the x-axis
custom_labels = ["Original", "Fictional", "Adversarial", "Contextual disguise"]
axes[0].set_xticks(range(len(custom_labels)))
axes[0].set_xticklabels(custom_labels, rotation=0, fontsize=12)

# Set the y-axis limit for the first plot
axes[0].set_ylim(0, 50)

# Annotate bar plot 1 with percentage values, highlighting "Adversarial"
for i, v in enumerate(percentage_correct.values):
    if i == 2:  # Assuming the last bar is "Adversarial"
        axes[0].text(i, v + 1, f"{v:.1f}%*", ha='center', va='bottom', fontweight='bold', fontsize=12)
    else:
        axes[0].text(i, v + 1, f"{v:.1f}%", ha='center', va='bottom', fontsize=12)

# Plot 2: Distribution of Problems Solved
axes[1].bar(solved_distribution.index, solved_distribution.values, color='gray', width=0.5)
axes[1].set_xlabel('Number of Variations Solved', fontsize=12)
axes[1].set_ylabel('Number of Problems', fontsize=12)

# Add horizontal grid lines
axes[1].yaxis.grid(True, linestyle='--', linewidth=0.7, color='gray')

# axes[1].set_title('Distribution of Problems Solved by Number of Variations', fontsize=16)
axes[1].set_xticks(range(0, 5))
axes[1].set_xticklabels(range(0, 5), fontsize=12)

# Set the y-axis limit for the second plot
axes[1].set_ylim(0, 2500)

# Annotate bar plot 2 with the number of problems
for i, v in enumerate(solved_distribution.values):
    axes[1].text(i, v + 10, str(v), ha='center', va='bottom', fontsize=12)

# Use tight layout to adjust padding
plt.tight_layout()

# Show the plots
plt.show()