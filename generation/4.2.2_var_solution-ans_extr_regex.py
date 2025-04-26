# Script for answer extraction from original and variation solutions
import pandas as pd
import re

def extract_numerical_answer(answer):
    """Extract numerical values from the answer column and return as a list of integers."""
    numbers = re.findall(r'-?\d+', str(answer))
    return [int(num) for num in numbers]

def extract_and_convert_answers(df):
    # Create new columns for regex-extracted answers
    answer_columns = ['original_ans', 'fictional_ans', 'adversarial_ans', 'contdis_ans']
    regex_columns = ['original_ans_regex', 'fictional_ans_regex', 'adversarial_ans_regex', 'contdis_ans_regex']

    # Initialize counters
    counters = {col: {'negative': 0, 'converted': 0, 'positive': 0, 'dropped': 0} for col in answer_columns}

    total_problems = len(df)
    row_index = 0  # Initialize a row index to access DataFrame rows directly

    for index, row in df.iterrows():
        for ans_col, regex_col in zip(answer_columns, regex_columns):
            answer = row[ans_col]
            numbers = extract_numerical_answer(answer)

            if len(numbers) == 1:
                num = numbers[0]
                if num == -1 or str(num).startswith('-10'):
                    # Negative answers that can't be converted
                    converted_answer = -1
                    counters[ans_col]['negative'] += 1
                elif num < 0:
                    # Convert other negative numbers to positive
                    converted_answer = abs(num)
                    counters[ans_col]['converted'] += 1
                else:
                    # Use positive numbers as is
                    converted_answer = num
                    counters[ans_col]['positive'] += 1
            else:
                # Non-numerical or complex/multiple answers default to -1
                converted_answer = -1
                counters[ans_col]['dropped'] += 1

            # Assign result to the new column
            df.at[index, regex_col] = converted_answer  # Use DataFrame indexing

        row_index += 1  # Increment the row index after each row is processed

        # Progress indication every 100 rows
        if (row_index) % 100 == 0 or row_index == total_problems:
            print(f"Processed {row_index} of {total_problems} rows.")

    # Ensure all columns are of integer type
    for regex_col in regex_columns:
        df[regex_col] = df[regex_col].astype(int)

    # Print summary statistics by variation
    for ans_col in answer_columns:
        print(f"\nFor column '{ans_col}':")
        print(f"Problems with negative answers (-1, -10,..): {counters[ans_col]['negative']}")
        print(f"Problems with negative answers automatically converted: {counters[ans_col]['converted']}")
        print(f"Problems with positive answers: {counters[ans_col]['positive']}")
        print(f"Problems dropped due to non-numerical or complex/multiple answers: {counters[ans_col]['dropped']}")
        total_processed = sum(counters[ans_col].values())
        print(f"Total number of problems processed and saved: {total_processed}")

    return df

def main():
    # Load the dataset from the parquet file
    df = pd.read_parquet('combinatorics_5583_sol_ans.parquet')

    # Extract and convert answers
    df = extract_and_convert_answers(df)

    # Save the updated DataFrame to new parquet and json files
    df.to_parquet('combinatorics_5583_sol_ans_regex.parquet', index=False)
    df.to_json('combinatorics_5583_sol_ans_regex.json', orient='records', lines=True)

if __name__ == '__main__':
    main()
