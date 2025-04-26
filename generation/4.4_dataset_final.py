# Replace answers with answer_regex + add problem_id

import pandas as pd


def process_dataframe(df):
    # Step 1: Remove specific columns
    columns_to_remove = ['original_ans', 'fictional_ans', 'adversarial_ans', 'contdis_ans']
    df.drop(columns=columns_to_remove, inplace=True)

    # Step 2: Rename columns
    columns_to_rename = {
        'original_ans_regex': 'original_ans',
        'fictional_ans_regex': 'fictional_ans',
        'adversarial_ans_regex': 'adversarial_ans',
        'contdis_ans_regex': 'contdis_ans'
    }
    df.rename(columns=columns_to_rename, inplace=True)

    # Step 3: Add "problem_id" and make it the first column
    df.insert(0, 'problem_id', range(len(df)))

    return df


def main():
    # Load the dataset from the parquet file
    df = pd.read_parquet('combinatorics_5583_sol_ans_regex.parquet')

    # Process the DataFrame
    df = process_dataframe(df)

    # Save the updated DataFrame to new parquet and json files
    output_filename = 'combinatorics_5583_final'
    df.to_parquet(f'{output_filename}.parquet', index=False)
    df.to_json(f'{output_filename}.json', orient='records', lines=True)


if __name__ == '__main__':
    main()
