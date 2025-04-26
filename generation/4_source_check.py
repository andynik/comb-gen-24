import pandas as pd


def count_problems_by_source(parquet_file_path):
    # Read the Parquet file into a DataFrame
    df = pd.read_parquet(parquet_file_path)

    # Check if the 'source' column exists
    if 'source' not in df.columns:
        print("The 'source' column is not found in the dataset.")
        return

    # Group by 'source' and count the number of problems from each source
    source_counts = df['source'].value_counts()

    # Print out the results
    for source, count in source_counts.items():
        print(f"Source: {source}, Problems: {count}")


# Path to your Parquet file
parquet_file_path = 'combinatorics4.2.2_solutions_with_regex_answers_test_1000.parquet'

# Call the function
count_problems_by_source(parquet_file_path)