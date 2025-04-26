import pandas as pd
import re
import textwrap


def extract_numerical_answer(answer):
    """Extract numerical values from the answer column and return as a list of integers."""
    numbers = re.findall(r'-?\d+', str(answer))
    return [int(num) for num in numbers]


def prompt_for_answer(problem, solution, current_answer):
    """Prompt the user for the correct answer, given a specific problem."""
    print("\nProblem Detected:")
    print("Problem Statement:")
    print(problem)
    print("Solution:", solution)
    print(f"Current Answer: {current_answer}")

    while True:
        try:
            user_input = int(input("Enter the correct answer (as a positive number): "))
            return abs(user_input)  # Ensure any input is positive
        except ValueError:
            print("Invalid input. Please enter an integer.")


def filter_problems_and_count(df):
    # Single positive, single negative conversions, manual confirmations
    confirmed_count = 0
    simple_conversion_count = 0
    positive_count = 0
    dropped_count = 0

    filtered_records = []

    for _, row in df.iterrows():
        numbers = extract_numerical_answer(row['answer'])

        if len(numbers) == 1:
            num = numbers[0]
            if num == -1 or str(num).startswith('-10'):
                filtered_row = row.to_dict()
                filtered_row['answer_regex'] = -1
                filtered_records.append(filtered_row)
                # Prompt the user for confirmation or a corrected answer
                # confirmed_answer = prompt_for_answer(row['problem'], row['solution'], num)
                # filtered_row = row.to_dict()
                # filtered_row['answer_regex'] = confirmed_answer
                # filtered_records.append(filtered_row)
                confirmed_count += 1
            elif num < 0:
                # Other negative numbers are converted to positive
                num = abs(num)
                filtered_row = row.to_dict()
                filtered_row['answer_regex'] = num
                filtered_records.append(filtered_row)
                simple_conversion_count += 1
            else:
                # Directly save positive numbers
                filtered_row = row.to_dict()
                filtered_row['answer_regex'] = num
                filtered_records.append(filtered_row)
                positive_count += 1
        else:
            dropped_count += 1

    print(f'\nProblems to be manually confirmed: {confirmed_count}')
    print(f'Problems with negative answers automatically converted: {simple_conversion_count}')
    print(f'Problems with positive answers: {positive_count}')
    print(f'Problems dropped due to non-numerical or complex/multiple answers: {dropped_count}')
    print(f'Total number of problems processed and saved: {confirmed_count + simple_conversion_count + positive_count}')

    return pd.DataFrame(filtered_records)


def main():
    # Load the dataset from parquet file
    df = pd.read_parquet('combinatorics2.parquet')

    # Filter the problems according to the criteria and count scenarios
    filtered_df = filter_problems_and_count(df)

    # Save the filtered results to new parquet and json files
    filtered_df.to_parquet('combinatorics3.parquet', index=False)
    filtered_df.to_json('combinatorics3.json', orient='records', lines=True)


if __name__ == '__main__':
    main()