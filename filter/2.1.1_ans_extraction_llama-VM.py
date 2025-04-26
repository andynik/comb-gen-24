import pandas as pd
import os
from llama_cpp import Llama

# Constants
MAX_PROBLEMS = 10148  # Adjust this later as needed for testing
LLAMA_MODEL_PATH = '/path-to-model/mathstral-7B-v0.1.Q4_K_M.gguf' # Path to the Llama model
MAX_TOKENS = 2048
GPU_PARAM = -1  # 0 for CPU, use negative values such as -1 for GPU

DATA_PATH = '/path-to-data/dataset.parquet'

def get_numerical_answer(problem_solution):
    try:
        if not os.path.isfile(LLAMA_MODEL_PATH):
            print(f"Error: Invalid model path '{LLAMA_MODEL_PATH}'")
            return "-"

        llm = Llama(model_path=LLAMA_MODEL_PATH, n_gpu_layers=GPU_PARAM, n_ctx=MAX_TOKENS)

        prompt = f"Please identify and extract the single numerical value that represents the final answer from the following text below. If there is no numerical answer, respond with '-'. Problem solution:\n {problem_solution}."
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
    total_problems = len(df)
    df = df.head(MAX_PROBLEMS if MAX_PROBLEMS > 0 else total_problems)  # Limit the number of problems for processing

    # Create a list to store the numerical answers
    answers = []

    for index, row in df.iterrows():
        solution = row['solution']
        numerical_answer = get_numerical_answer(solution)

        # Print the result for each problem
        print(f"Extracting answer from problem {index + 1}: {numerical_answer}")

        answers.append(numerical_answer)

        # Save temporary files every 1000 problems
        if (index + 1) % 1000 == 0 or (index + 1) == total_problems:
            temp_df = df.iloc[max(0, index - 999):index + 1]
            temp_df['answer'] = answers[-len(temp_df):]
            temp_filename = f'combinatorics_temp_{index + 1}.parquet'
            temp_df.to_parquet(temp_filename)
            print(f"Temporary file saved: {temp_filename}")

    # Append the new 'answer' column to the DataFrame
    df['answer'] = answers

    # Save the new DataFrame to a new parquet file
    output_parquet_path = 'combinatorics2.parquet'
    df.to_parquet(output_parquet_path)
    print(f"Final file saved: {output_parquet_path}")

    # Also save the DataFrame to a json file
    output_json_path = 'combinatorics2.json'
    df.to_json(output_json_path, orient='records', lines=True)
    print(f"Final JSON saved: {output_json_path}")

if __name__ == "__main__":
    main()
