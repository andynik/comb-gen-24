import pandas as pd
import openai
import os

# Set your OpenAI API Key
os.environ["OPENAI_API_KEY"] = "Your_key"
client = openai.OpenAI()

# Constants
PROBLEM_FILE = 'combinatorics3_variations_5583.parquet'
MODEL_NAME_SOLUTION = "gpt-4o-mini"
MAX_PROBLEMS = -1  # Set to -1 to process all problems or specify a number for a subset

# Starting index for processing
START_INDEX = 5582  # Start processing from problem (0-based index)


def get_full_solution(problem_statement):
    """Gets the full solution of the problem statement using OpenAI's API."""
    try:
        conversation = [
            {"role": "user", "content": f"Solve the following mathematical problem."
                                        f"Return solution with the final numerical answer at the end."
                                        f"Problem: {problem_statement}"}
        ]
        response = client.chat.completions.create(
            model=MODEL_NAME_SOLUTION,
            messages=conversation
        )
        solution = response.choices[0].message.content.strip()
        return solution
    except Exception as e:
        print(f"Error getting full solution: {e}")
        return "-"


def main():
    # Read the dataset
    df = pd.read_parquet(PROBLEM_FILE)

    # Modify the DataFrame to start processing from the START_INDEX
    df = df.iloc[START_INDEX:]

    # If MAX_PROBLEMS is set to a positive number, slice the DataFrame further
    if MAX_PROBLEMS > 0:
        df = df.head(MAX_PROBLEMS)

    # Create lists to store solutions
    original_sol = []
    fictional_sol = []
    adversarial_sol = []
    condits_sol = []

    # Initialize separate counter for processed problems
    counter = 0

    for _, row in df.iterrows():
        counter += 1
        problem_number = START_INDEX + counter
        print(f"Processing problem {problem_number}/{START_INDEX + len(df)}")

        # Generate full solutions for each problem and its variations
        original_sol.append(get_full_solution(row['problem']))
        fictional_sol.append(get_full_solution(row['fictional']))
        adversarial_sol.append(get_full_solution(row['adversarial']))
        condits_sol.append(get_full_solution(row['contdis']))

        # Save progress every 1,000 problems
        if counter % 100 == 0 or counter == len(df):
            # Append the solutions to the DataFrame up to the current point
            temp_df = df.iloc[:counter]
            temp_df['original_sol'] = original_sol
            temp_df['fictional_sol'] = fictional_sol
            temp_df['adversarial_sol'] = adversarial_sol
            temp_df['contdis_sol'] = condits_sol

            temp_filename = f'combinatorics_progress_{problem_number}.parquet'
            temp_df.to_parquet(temp_filename)
            print(f"Checkpoint saved: {temp_filename}")

    # Append final solutions to the DataFrame
    df['original_sol'] = original_sol
    df['fictional_sol'] = fictional_sol
    df['adversarial_sol'] = adversarial_sol
    df['contdis_sol'] = condits_sol

    # Save the final DataFrame to a parquet file
    df.to_parquet('combinatorics5_solutions_5583.parquet')

    # Also save the DataFrame to a json file
    # df.to_json('combinatorics5_solutions_5583.json', orient='records', lines=True)


if __name__ == "__main__":
    main()