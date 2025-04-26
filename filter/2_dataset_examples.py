import pandas as pd
import textwrap

# Define the maximum width for each line
MAX_LINE_WIDTH = 80  # You can adjust this value as needed

# Specify the path to the JSON file
json_file_path = 'combinatorics3.json'

# Read the JSON file into a DataFrame
df = pd.read_json(json_file_path, orient='records', lines=True)

# Select only the "source" and "problem" columns
# df_selected = df[['source', 'problem', 'solution']]
# df_selected = df[['source', 'problem', 'solution', 'answer']]
df_selected = df[['source', 'problem', 'solution', 'answer_regex']]


# Function to print text with wrapping
def print_wrapped(text, max_width):
    for wrapped_line in textwrap.wrap(text, width=max_width):
        print(wrapped_line)

# Print examples from the selected DataFrame
def print_examples(df, num_examples=5, max_width=MAX_LINE_WIDTH):
    for idx, row in df.head(num_examples).iterrows():
        print(f"Source ({idx + 1}):", row['source'])
        print(f"Source ({idx + 1}):", row['answer_regex'])
        print("Problem:")
        print_wrapped(row['problem'], max_width)
        print("Solution:")
        print_wrapped(row['solution'], max_width)
        print("-" * max_width)  # Separator line


# Print the first few rows (examples) from the DataFrame
print("Examples from the combinatorics.json file (source and problem columns):")
print_examples(df_selected, num_examples=100)
