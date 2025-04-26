# # problem include "how many", solution include combinatorial terms but exclude algebra terms

import os
import pandas as pd

# Define the folder containing the Parquet files
data_folder = 'data'

# Define the specific phrase and combinatorial keywords
how_many_phrase = "how many"
combinatorial_keywords = [
    "permutation", "combination", "factorial", "binomial", "arrangement",
    "combinatorial", "counting", "probability", "pigeonhole", "partition",
    "matching", "graph", "vertex", "edge", "subsets", "enumerate"
]

# Define algebra-related keywords for exclusion
algebra_keywords = [
    "equation", "solve", "variable", "algebra", "expression", "polynomial",
    "quadratic", "linear", "factor", "inequality", "terms", "coefficient", "function"
]

# Function to check for the phrase "how many" in the "problem" column
def contains_how_many(row):
    problem_text = str(row['problem']).lower()
    return how_many_phrase in problem_text

# Function to check for combinatorial terminology in the "solution" column
def contains_combinatorial_terms(row):
    solution_text = str(row['solution']).lower()
    return any(keyword in solution_text for keyword in combinatorial_keywords)

# Function to check for algebra-related terms in both columns
def is_algebra_related(row):
    combined_text = (str(row['problem']) + " " + str(row['solution'])).lower()
    return any(keyword in combined_text for keyword in algebra_keywords)

# Initialize a list to store the filtered DataFrames
filtered_df_list = []

# Variables to track progress
total_files = len([file_name for file_name in os.listdir(data_folder) if file_name.endswith(".parquet")])
processed_files = 0
total_filtered_rows = 0

# Iterate over all Parquet files in the data folder
for file_name in os.listdir(data_folder):
    if file_name.endswith(".parquet"):
        file_path = os.path.join(data_folder, file_name)

        # Read the Parquet file into a DataFrame
        df = pd.read_parquet(file_path)

        # Step 1: Filter for "how many" in the "problem" column
        how_many_filtered_df = df[df.apply(lambda row: contains_how_many(row), axis=1)]

        # Step 2: Among the filtered, check for combinatorial terms in the "solution" column
        combinatorial_filtered_df = how_many_filtered_df[
            how_many_filtered_df.apply(lambda row: contains_combinatorial_terms(row), axis=1)
        ]

        # Step 3: Exclude algebra-related problems
        non_algebra_df = combinatorial_filtered_df[
            ~combinatorial_filtered_df.apply(lambda row: is_algebra_related(row), axis=1)
        ]

        # Append the filtered DataFrame to the list
        filtered_df_list.append(non_algebra_df)

        # Update progress tracking variables
        processed_files += 1
        total_filtered_rows += len(non_algebra_df)

        # Print status update
        print(f"Processed file {processed_files}/{total_files}: {file_name} - {len(non_algebra_df)} filtered rows")

# Concatenate all filtered DataFrames
all_filtered_df = pd.concat(filtered_df_list, ignore_index=True)

# Save the filtered results to a new Parquet file
output_parquet_path = 'combinatorics_non_algebra.parquet'
all_filtered_df.to_parquet(output_parquet_path)

# Save the filtered results to a new JSON file
output_json_path = 'combinatorics_non_algebra.json'
all_filtered_df.to_json(output_json_path, orient='records', lines=True)

# Print final status
print(f"\nTotal files processed: {processed_files}")
print(f"Total filtered rows: {total_filtered_rows}")
print(f"Filtered data saved to {output_parquet_path} and {output_json_path}")