# to check problems where -1 was received as answer_regex

import pandas as pd
import textwrap
import re

# Define the maximum width for each line
MAX_LINE_WIDTH = 80

# Specify the path to the JSON file
json_file_path = 'combinatorics3.json'

# Read the JSON file into a DataFrame
df = pd.read_json(json_file_path, orient='records', lines=True)

# Add a new 'originally_negative' column to track which answers were negative initially
df['originally_negative'] = df.apply(lambda row: any(int(num) < 0 for num in re.findall(r'-?\d+', str(row['answer_regex']))), axis=1)

# Filter the DataFrame to include only the problems where the answer was originally negative
df_negative_answers = df[df['originally_negative']]

# Count how many problems had an originally negative answer
num_negative_answers = len(df_negative_answers)

# Select only the relevant columns for display
df_selected = df_negative_answers[['source', 'problem', 'solution', 'answer', 'answer_regex']]

# Function to print text with wrapping
def print_wrapped(text, max_width):
    for wrapped_line in textwrap.wrap(text, width=max_width):
        print(wrapped_line)

# Print examples from the selected DataFrame
def print_examples(df, num_examples, max_width=MAX_LINE_WIDTH):
    for idx, row in df.head(num_examples).iterrows():
        print(f"Source ({idx + 1}):", row['source'])
        print(f"Original Answer ({idx + 1}):", row['answer'])
        print(f"Answer Regex ({idx + 1}):", row['answer_regex'])
        print("Problem:")
        print_wrapped(row['problem'], max_width)
        print("Solution:")
        print_wrapped(row['solution'], max_width)
        print("-" * max_width)  # Separator line

# Print the number of problems with originally negative answers
print(f"Number of problems with originally negative answers: {num_negative_answers}\n")

# Print the first few rows (examples) from the DataFrame
print("Examples of problems with originally negative answers:")
print_examples(df_selected, num_examples=num_negative_answers)
