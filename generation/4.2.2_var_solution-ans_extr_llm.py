### Script 2: Answer Extraction (llm-based)

import pandas as pd
import os
from llama_cpp import Llama

# Constants
LLAMA_MODEL_PATH = '/path-to-model/mathstral-7B-v0.1.Q4_K_M.gguf'  # Path to the Llama model
MAX_TOKENS = 2048
GPU_PARAM = -1  # 0 for CPU, use negative values for GPU
DATA_PATH = '/path-to-dataset/dataset.parquet'
NUM_PROBLEMS_TO_PROCESS = -1  # Set to -1 to process all problems

def get_numerical_answer(solution):
    try:
        if not os.path.isfile(LLAMA_MODEL_PATH):
            print(f"Error: Invalid model path '{LLAMA_MODEL_PATH}'")
            return "-"

        llm = Llama(model_path=LLAMA_MODEL_PATH, n_gpu_layers=GPU_PARAM, n_ctx=MAX_TOKENS)

        prompt = (f"Please identify and extract the single numerical value that represents the final answer"
                  f"from the following text below. If there is no numerical answer, respond with '-'."
                  f"Problem solution:\n {solution}.")
        user_input = f"Q: {prompt} A:"

        print(f"Processing: {prompt}")

        response = llm(user_input, max_tokens=MAX_TOKENS, stop=["Q:"], echo=True)
        result_text = response["choices"][0]["text"].replace(user_input, "").strip()

        return result_text if result_text else "-"
    except Exception as e:
        print(f"Error: {e}")
        return "-"


def main():
    # Read the dataset
    df = pd.read_parquet(DATA_PATH)

    # Limit the number of problems if specified
    if NUM_PROBLEMS_TO_PROCESS != -1:
        df = df.head(NUM_PROBLEMS_TO_PROCESS)

    # Column pairs for solutions and answers
    columns_pairs = [
        ('original_sol', 'original_ans'),
        ('fictional_sol', 'fictional_ans'),
        ('adversarial_sol', 'adversarial_ans'),
        ('contdis_sol', 'contdis_ans')
    ]

    # Process each pair of solution and answer columns
    for sol_col, ans_col in columns_pairs:
        answers = []
        for index, row in df.iterrows():
            solution = row[sol_col]
            numerical_answer = get_numerical_answer(solution)
            print(f"Extracting answer from {sol_col} for problem {index + 1}: {numerical_answer}")
            answers.append(numerical_answer)

        # Add the new answers to the DataFrame
        df[ans_col] = answers

    # Save the new DataFrame to a new parquet file
    output_parquet_path = 'combinatorics5_solutions_with_answers.parquet'
    df.to_parquet(output_parquet_path)
    print(f"Final PARQUET file saved: {output_parquet_path}")

    # Also save the DataFrame to a json file
    output_json_path = 'combinatorics5_solutions_with_answers.json'
    df.to_json(output_json_path, orient='records', lines=True)
    print(f"Final JSON saved: {output_json_path}")


if __name__ == "__main__":
    main()