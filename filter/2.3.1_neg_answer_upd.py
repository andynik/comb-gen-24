# additional script to replace -1 with values from the manually checked file

import pandas as pd

# Load the JSON files with `lines=True` in case they are line-oriented
df_main = pd.read_json('combinatorics3.json', lines=True)
df_negative = pd.read_json('combinatorics3_negative.json', lines=True)

# Initialize a counter for successful changes
successful_changes = 0

# Identify rows where "answer_regex" is -1 in the main file
to_update = df_main['answer_regex'] == -1

# For those rows, find the corresponding problem in the negative file
# and use its "answer_regex" to update the main DataFrame
for index, row in df_main[to_update].iterrows():
    # Match based on the "problem" column or any other identifier
    problem = row['problem']

    # Find the corresponding row in the negative DataFrame
    corresponding_negative = df_negative[df_negative['problem'] == problem]

    if not corresponding_negative.empty:
        # Assuming there's a one-to-one match and taking the first (and assuming only) match
        updated_answer_regex = corresponding_negative.iloc[0]['answer_regex']
        df_main.at[index, 'answer_regex'] = updated_answer_regex
        # Increment the counter for each successful change
        successful_changes += 1

# Save the updated main DataFrame to a Parquet file
df_main.to_parquet('combinatorics3.parquet')

# Save the updated main DataFrame back to JSON
df_main.to_json('combinatorics3.json', orient='records', lines=True) # , indent=4 to make it nice-looking

# Output the number of successful changes
print(f"Number of successful changes: {successful_changes}")