import pandas as pd
import os

# Define the directory containing the parquet files and the base output file name
input_directory = "solutions"
output_parquet_file = "combinatorics_sol_ans_5583.parquet"
output_json_file = "combinatorics_sol_ans_5583.json"

# List of files in the order you want to combine them
files_to_merge = [
    "combinatorics_solutions_0-999_with_answers.parquet",
    "combinatorics_solutions_1000-1999_with_answers.parquet",
    "combinatorics_solutions_2000-2999_with_answers.parquet",
    "combinatorics_solutions_3000-3999_with_answers.parquet",
    "combinatorics_solutions_4000-4999_with_answers.parquet",
    "combinatorics_solutions_5000-5583_with_answers.parquet"
]

# Initialize an empty list to hold DataFrame chunks
dataframes = []

# Loop over each file, read it and append to the list
for file_name in files_to_merge:
    file_path = os.path.join(input_directory, file_name)
    df = pd.read_parquet(file_path)
    dataframes.append(df)

# Concatenate all dataframes
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a new parquet file
combined_df.to_parquet(output_parquet_file)
print(f"Parquet file has been successfully saved to {output_parquet_file}")

# Save the combined DataFrame to a new JSON file
combined_df.to_json(output_json_file, orient='records', lines=True)
print(f"JSON file has been successfully saved to {output_json_file}")
